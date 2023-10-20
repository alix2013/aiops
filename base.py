# llm server base functions, access LLM and vectorDB

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import Ollama
from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import torch
import os 
from dotenv import load_dotenv
import logging
import platform
from langchain.memory import ConversationBufferMemory

# get device type base on current GPU and platform
def getDeviceType():
    device_type="cuda" if torch.cuda.is_available() else "cpu"
    device_type="mps" if platform.machine() == "arm64" else "cpu"
    return device_type 

if not load_dotenv():
    print("Load .env file failed . Please check if it exists")
    exit(1)

EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL_NAME","hkunlp/instructor-large")
DB_DIRECTORY = os.environ.get('DB_DIRECTORY', "./DB")
MODEL_NAME = os.environ.get('MODEL_NAME',"mistral:latest")
LLM_SERVER_URL = os.environ.get('LLM_SERVER_URL',"http://localhost:11434")
MODEL_TEMPERATURE=float(os.environ.get('MODEL_TEMPERATURE',"0.2"))

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
)

logging.info(f"MODEL_NAME: {MODEL_NAME}")
logging.info(f"MODEL_TEMPERATURE: {MODEL_TEMPERATURE}")
logging.info(f"DB_DIRECTORY: {DB_DIRECTORY}")
logging.info(f"EMBEDDING_MODEL_NAME: {EMBEDDING_MODEL_NAME}")
logging.info(f"LLM_SERVER_URL: {LLM_SERVER_URL}")
logging.info(f"device_type: {getDeviceType()}")


# get vectorstore
def getVectorDB():
    device_type = getDeviceType()
    embeddings = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": device_type})
    vectorstore = Chroma(
        persist_directory=DB_DIRECTORY,
        embedding_function=embeddings,
    )
    return vectorstore

# get prompt template
def getPromptTemplate(useHistory=False):
    system_prompt = """You are a helpful assistant, you will use the provided context to answer user questions.
Read the given context before answering questions and think step by step. If you can not answer a user question based on 
the provided context, inform the user. Do not use any other information for answering user. Provide a detailed answer to the question."""
  
    if "llama" in MODEL_NAME.lower():
        BEGIN_INST, END_INST = "[INST]", "[/INST]"
        BEGIN_SYS, END_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        SYSTEM_PROMPT = BEGIN_SYS + system_prompt + END_SYS
        if useHistory:
            instruction = """
            Context: {history} \n {context}
            User: {question}"""
            template = BEGIN_INST + SYSTEM_PROMPT + instruction + END_INST

            promptTemplate = PromptTemplate(
                input_variables=["context", "question", "history"],
                template=template,
            )
            logging.debug(f"llama template:{template}")

            return promptTemplate
        else:
            instruction = """
            Context: {context}
            User: {question}"""
            template = BEGIN_INST + SYSTEM_PROMPT + instruction + END_INST

            promptTemplate = PromptTemplate(
                input_variables=["context", "question" ],
                template=template,
            )
            logging.debug(f"llama template:{template}")

            return promptTemplate

    elif "mistral" in MODEL_NAME.lower():
        BEGIN_INST, END_INST = "[INST]", "[/INST]"
        if useHistory:
            instruction = """
            Context: {history} \n {context}
            User: {question}"""
            # template = "<s>"+ BEGIN_INST + system_prompt + instruction + END_INST
            template =  BEGIN_INST + system_prompt + instruction + END_INST
            promptTemplate = PromptTemplate(
                input_variables=["context", "question", "history"],
                template=template,
            )
            logging.debug(f"mistral template:{template}")
            return promptTemplate
        else: 
            instruction = """
            Context: {context}
            User: {question}"""

            # template = "<s>"+ BEGIN_INST + system_prompt + instruction + END_INST
            template =  BEGIN_INST + system_prompt + instruction + END_INST
            promptTemplate = PromptTemplate(
                input_variables=["context", "question" ],
                template=template,
            )
            logging.debug(f"mistral template:{template}")
            return promptTemplate
    else:
        template = system_prompt + """
                Context: \n {context}
                User: {question}
                Answer:"""
        promptTemplate = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

        logging.debug(f"mistral template:{template}")
        return promptTemplate

# get LLM Model
def getModel(llmServerUrl=LLM_SERVER_URL,model_name=MODEL_NAME):
    #chat_model = ChatOllama(base_url=llmServerUrl,
    chat_model = ChatOllama(base_url=llmServerUrl,
                        model=model_name,
                        temperature=MODEL_TEMPERATURE,
                        # verbose=True,
                        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    return chat_model 

# get RetrievalQA 
def getQA(useHistory=False):
    promptTemplate = getPromptTemplate(useHistory)
    model = getModel()
    vectorstore = getVectorDB()
    if useHistory:
        memory = ConversationBufferMemory(input_key="question", memory_key="history")
        return RetrievalQA.from_chain_type(
            model,
            retriever=vectorstore.as_retriever(),
            # retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 8}),
            # retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .9}),

            return_source_documents=True,
            chain_type_kwargs={"prompt": promptTemplate, "memory": memory},
        )
    else:
        return RetrievalQA.from_chain_type(
            model,
            retriever=vectorstore.as_retriever(),
            # retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 8}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": promptTemplate },
        )


def getQAFromLLM(model=getModel(), promptTemplate=getPromptTemplate(True), vectorstore=getVectorDB()):
    # promptTemplate = getPromptTemplate(useHistory)
    # model = getModel()
    # vectorstore = getVectorDB()
    memory = ConversationBufferMemory(input_key="question", memory_key="history")
    return RetrievalQA.from_chain_type(
        model,
        retriever=vectorstore.as_retriever(),
        # retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 8}),
#        retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": promptTemplate, "memory": memory},
    )
