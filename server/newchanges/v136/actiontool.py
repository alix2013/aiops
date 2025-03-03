import logging
import subprocess
import sys
import os 

from llmbase import getModel
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
)

ACTION_MODEL_NAME = os.environ.get('ACTION_MODEL_NAME',"neural-chat:latest")
ACTION_MODEL_TEMPERATURE = float(os.environ.get('ACTION_MODEL_TEMPERATURE',"0.2"))

logging.info(f"ACTION_MODEL_NAME={ACTION_MODEL_NAME}")
logging.info(f"ACTION_MODEL_TEMPERATURE={ACTION_MODEL_TEMPERATURE}")

def askAIAction(question):
    logging.info(f"Question:{question}")
    llm = getModel(model_name=ACTION_MODEL_NAME,temperature=ACTION_MODEL_TEMPERATURE)
    prompt = PromptTemplate(
        input_variables=["question"],
        template="""you are kubernetes administrator, answer the questions, please follow the rules:
1. understand question, use kubectl command to answer question and only respond the kubectl command line without further explanations,
so that it's easy to copy the command to run in shell. 
2. if no namespaces specified, use "default"
3. returned command should not block the shell complete quickly, for example, Do not use -f to view logs, it will block the output 
4. if provided information is not enough to generate the command, please respond: 
I need more information to decide next step and state what information you need
Here are some examples:
question: list all pod
kubectl get pod 
question: show pod mypod
kubectl describe pod mypod 
question: show logs 
I need more information to decide next step, what is the deployment or pod name you want to view the log
question: show log of deployment chatserver
kubectl logs deployment/chatserver 
question: show log of pod mypod in namespace test
kubectl logs mypod  -n test

current question: {question} 
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    answer=str(chain.run(question))
    return answer


def precheckAction(action):
    logging.info(f"precheck action:{action}")
    words = action.strip().split(" ")
    # logging.info(words)
    if words[0] == "kubectl":
        cmd = "oc " + " ".join(words[1:])
        # logging.info("cmd:",cmd)
        logging.info(f"return cmd from precheck:{cmd}")
        return 0,cmd
    elif words[0] == "I":
        return 1, action
    else:
        return -1, "precheck failed"


def runCmd(cmd):
    # logging.info("cmd:",cmd)
    logging.info(f"Run cmd:{cmd}")
    cmdList = cmd.split(" ")
    # process = subprocess.Popen(cmdList, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    # return_value = process.returncode
    # if return_value == 0:
    #     return 0, stdout 
    # else:
    #     return return_value, stderr
    result = subprocess.run(cmdList, bufsize=0, capture_output=True, timeout=15)
    if result.returncode != 0 :
       oc_result = result.stderr.decode()
       return 1, oc_result
    else: 
      oc_result = result.stdout.decode()
      return 0,oc_result


def checkIfAction(action):
    logging.info(f"check action:{action}")
    words = action.strip().split(":")
    if len(words) > 0 and words[0].strip() == "/action":
        retValue = " ".join(words[1:])
        # logging.info(retValue)
        return True, retValue
    else:
        logging.info(f"Not action:{action}")
        return False, action

def runAction(question):
    isAction,act = checkIfAction(question) 

    if isAction==False: 
        return "Not valide action"
    action = askAIAction(act)  

    logging.info(f"get action from AI:{action}")
    retcode, cmd = precheckAction(action)

    logging.info(f"precheck result: retcode:{retcode}, {cmd}")
    if retcode == 0:
      _,result = runCmd(cmd)
      return result
    elif retcode == 1:
      return cmd
    else: 
      return "Current version not support this action, please contact administrator"

if __name__ == "__main__":
    args = [*sys.argv[1:]]  
    # print(args)
    if len(args) > 0:
        print(runAction(" ".join(args)))
    else:
        print("Need input parameters with /action: as prefix")
