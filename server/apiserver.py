from flask_cors import CORS
import os
import logging
from flask import Flask, jsonify, request, Response
from llmbase import getModel, getQA, ask_llm_question
from actiontool import checkIfAction, runAction
from streamcallback  import CustStreamHandler
import threading
import json

app = Flask(__name__)
CORS(app)
cache = {}

QA = getQA()
llm = getModel()

# qa4stream, qa4stramLLM = getQAandLLM()

def askllm(question):
    return ask_llm_question(llm,question)

def ask(question):
    result = QA({"query": question})
    return result

@app.route("/", methods=["GET"])
def default_handler():
    return "apiserver is running" 

@app.route("/ask", methods=["POST"])
def askAI():
    request_data = request.get_json()
    user_prompt = request_data.get("request")
    if user_prompt:
        # run action
        isAction, act = checkIfAction(user_prompt)
        if ( isAction == True ):
            print(f"run action: {act}" )
            answer = runAction(user_prompt)
            prompt_response_dict = {
                "request": user_prompt,
                "response": answer,
            }
            return jsonify(prompt_response_dict), 200
        # return from simple cache
        if user_prompt in cache:
            prompt_response_dict = cache[user_prompt]
            print("return from cache")
            return jsonify(prompt_response_dict), 200
        res = ask(user_prompt)
        answer, docs = res["result"], res["source_documents"]

        prompt_response_dict = {
            "request": user_prompt,
            "response": answer,
        }

        prompt_response_dict["source"] = []
        for document in docs:
            prompt_response_dict["source"].append(
                (os.path.basename(str(document.metadata["source"])), str(document.page_content))
            )
        print(prompt_response_dict)
        cache[user_prompt] = prompt_response_dict
        return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 600

@app.route("/ask4pd", methods=["POST"])
def askAI4pd():
    request_data = request.get_json()
    user_prompt = request_data.get("request")
    if user_prompt:
        # return from simple cache
        if user_prompt in cache:
            prompt_response_dict = cache[user_prompt]
            print("return from cache")
            return jsonify(prompt_response_dict), 200
        prompt_prefix = "Hi, I get the following information,please give me some relevant information about it and suggestions to solve it:\n"
        new_user_prompt = prompt_prefix + user_prompt
        res = ask(new_user_prompt)
        answer, docs = res["result"], res["source_documents"]
        prompt_response_dict = {
            "request": user_prompt,
            "response": answer,
        }

        prompt_response_dict["source"] = []
        for document in docs:
            prompt_response_dict["source"].append(
                (os.path.basename(str(document.metadata["source"])), str(document.page_content))
            )
        print(prompt_response_dict)
        cache[user_prompt] = prompt_response_dict

        return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 600

@app.route("/sum", methods=["POST"])
def askAI4sum():
    request_data = request.get_json()
    user_prompt = request_data.get("request")
    if user_prompt:
        # return from simple cache
        if user_prompt in cache:
            prompt_response_dict = cache[user_prompt]
            print("return from cache")
            return jsonify(prompt_response_dict), 200
        prompt_prefix = "Write a concise summary of the following:\n"
        new_user_prompt = prompt_prefix + user_prompt
        answer = askllm(new_user_prompt)
        prompt_response_dict = {
            "request": user_prompt,
            "response": answer,
        }
        print(prompt_response_dict)
        cache[user_prompt] = prompt_response_dict

        return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 600


@app.route("/askany", methods=["POST"])
def askAI4any():
    request_data = request.get_json()
    user_prompt = request_data.get("request")
    if user_prompt:
        # return from simple cache
        if user_prompt in cache:
            prompt_response_dict = cache[user_prompt]
            print("return from cache")
            return jsonify(prompt_response_dict), 200
        prompt_prefix = ""
        new_user_prompt = prompt_prefix + user_prompt
        answer = askllm(new_user_prompt)
        prompt_response_dict = {
            "request": user_prompt,
            "response": answer,
        }
        print(prompt_response_dict)
        cache[user_prompt] = prompt_response_dict

        return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 600

# callbackHandler = CustStreamHandler()
# qastream=getQA(streamCallback=callbackHandler)


## stream output
# def async_run(qa, question):
#     # qa({"query": question}, return_only_outputs=True)
#     qa({"query": question} )

# def streamQA(question):
#     callbackHandler = CustStreamHandler()
#     qa = getQA(streamCallback=callbackHandler)
#     thread = threading.Thread(target=async_run, args=(qa, question))
#     thread.start()

#     return callbackHandler.generate_tokens()

#     # for value in callbackHandler.generate_tokens():
#     #     data = {
#     #                 "request": question,
#     #                 "response": value
#     #             }
#     #     yield f"{json.dumps(data)}\n\n"



def formatQAResult(qaResult):
    question, answer, sourceDocs = qaResult['query'],qaResult["result"], qaResult["source_documents"]
    # retMsg = f"{answer}\n---\n***HERE ARE REFERENCED SOURCE DOCUMENTS***\n "
    # for i, document in enumerate(sourceDocs):
    #   source = os.path.basename(str(document.metadata['source'])) 
    #   retMsg = retMsg + f"{i+1}.{source}:\n```{document.page_content}\n```\n "
    doc_sourceList = []
    for i, document in enumerate(sourceDocs):
      source = os.path.basename(str(document.metadata['source'])) 
      doc = {
              "source": source,
              "page_content": document.page_content
              }
      # retMsg = retMsg + f"{i+1}.{source}:\n```{document.page_content}\n```\n "
      doc_sourceList.append(doc)

    data = { 
            "question": question,
            "answer" : answer,
            "source" : doc_sourceList,
            "finished": True
            }
    return f"{json.dumps(data)}\n"

def streamQA(question):
    callbackHandler = CustStreamHandler()
    qa = getQA(streamCallback=callbackHandler)
    # qa4stramLLM.callback_manager.set_handler(handler=callbackHandler)

    # def async_run(qa, question):
    #   # qa({"query": question}, return_only_outputs=True)
    #   return qa({"query": question} )

    # result = {"result":None}
    # def run_qa_save_result(func, *args):
    #   result['result'] = func(*args)
    #   print(result['result'])

    # # thread = threading.Thread(target=async_run, args=(qa, question))
    # thread = threading.Thread(target=run_qa_save_result, args=(async_run,qa,question))

    result = {"result":None}
    def run_qa_save_result(qa, question):
      result['result'] = qa({"query": question} )
      print(result['result'])

    thread = threading.Thread(target=run_qa_save_result, args=(qa,question))
    thread.start()

    # generate result
    def generator():
       answer = ""
       for t in callbackHandler.generate_tokens():
         # yield t
         answer = answer + t
         data = { 
            "question": question,
            "answer": answer,
            "delta" : t,
            "finished": False
            }
         yield f"{json.dumps(data)}\n"
       # yield result['result']
       if (result['result']): 
         # yield f"{json.dumps(result['result'])}\n\n"
         yield formatQAResult(result['result'])

    return generator()
    # return callbackHandler.generate_tokens()

    # for value in callbackHandler.generate_tokens():
    #     data = {
    #                 "request": question,
    #                 "response": value
    #             }
    #     yield f"{json.dumps(data)}\n\n"


def streamllm(question):
    callbackHandler = CustStreamHandler()
    # llm.callback_manager.set_handler(callbackHandler)
    llm = getModel(streamCallback=callbackHandler)
    thread = threading.Thread(target=ask_llm_question, args=(llm,question))
    thread.start()
    # return callbackHandler.generate_tokens()
    answer=""
    for value in callbackHandler.generate_tokens():
        answer += value
        data = {
                    "question": question,
                    "delta": value,
                    "answer": answer,
                    "finished": False
                }
        yield f"{json.dumps(data)}\n"

    finaldata = {
                    "question": question,
                    "delta": "",
                    "answer": answer,
                    "finished": True
                }
    yield f"{json.dumps(finaldata)}"

@app.route('/stream/ask', methods=["POST"])
def streamask():
    request_data = request.get_json()
    user_prompt = request_data.get("request")
    if user_prompt:
        return Response(streamQA(user_prompt), mimetype="text/event-stream")
    else:
        return "No user prompt received", 401

@app.route('/stream/askany', methods=["POST", "GET"])
def streamaskany():
    request_data = request.get_json()
    user_prompt = request_data.get("request")
    if user_prompt:
        return Response(streamllm(user_prompt), mimetype="text/event-stream")
    else:
        return "No user prompt received", 401


@app.route("/stream/sum", methods=["POST"])
def askAI4sum_stream():
    request_data = request.get_json()
    user_prompt = request_data.get("request")
    if user_prompt:
        prompt_prefix = "Write a concise summary of the following:\n"
        new_user_prompt = prompt_prefix + user_prompt
        return Response(streamllm(new_user_prompt), mimetype="text/event-stream")
        # answer = askllm(new_user_prompt)
        # prompt_response_dict = {
        #     "request": user_prompt,
        #     "response": answer,
        # }
        # print(prompt_response_dict)
        # cache[user_prompt] = prompt_response_dict

        # return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 401

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    app.run(debug=False, port=int(os.environ.get("PORT","5001")), host="0.0.0.0")


