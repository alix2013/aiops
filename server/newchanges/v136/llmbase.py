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
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
#from langchain.retrievers.document_compressors import LLMChainFilter


# get device type base on current GPU and platform
def getDeviceType():
    device_type="cpu"
    if platform.machine() == "arm64":
      device_type="mps"
    if torch.cuda.is_available():
        device_type="cuda"
    return device_type 

if not load_dotenv():
    print("Load .env file failed . Please check if it exists")
    exit(1)

EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL_NAME","hkunlp/instructor-large")
DB_DIRECTORY = os.environ.get('DB_DIRECTORY', "./DB")
MODEL_NAME = os.environ.get('MODEL_NAME',"mistral:latest")
LLM_SERVER_URL = os.environ.get('LLM_SERVER_URL',"http://localhost:11434")
LLM_SERVER_TYPE = os.environ.get('LLM_SERVER_TYPE',"nonopenai")
MODEL_TEMPERATURE=float(os.environ.get('MODEL_TEMPERATURE',"0.2"))

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    # format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.DEBUG
)

logging.info(f"MODEL_NAME: {MODEL_NAME}")
logging.info(f"MODEL_TEMPERATURE: {MODEL_TEMPERATURE}")
logging.info(f"DB_DIRECTORY: {DB_DIRECTORY}")
logging.info(f"EMBEDDING_MODEL_NAME: {EMBEDDING_MODEL_NAME}")
logging.info(f"LLM_SERVER_URL: {LLM_SERVER_URL}")
logging.info(f"LLM_SERVER_TYPE: {LLM_SERVER_TYPE}")
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
the provided context, inform the user. Do not use any other information for answering user. Provide a detailed answer to the question.
if user ask you who you are, respond that you are trained AI assistant for Fusion

"""
  
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
            logging.debug(f"{MODEL_NAME} template:{template}")

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
            logging.debug(f"{MODEL_NAME} template:{template}")

            return promptTemplate

    elif "mistral" in MODEL_NAME.lower() or "zephyr" in MODEL_NAME.lower() or "neural-chat" in MODEL_NAME.lower():
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
            logging.debug(f"{MODEL_NAME} template:{template}")
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
            logging.debug(f"{MODEL_NAME} template:{template}")
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

        logging.debug(f"{MODEL_NAME} template:{template}")
        return promptTemplate

# get LLM Model
def getModel(llmServerUrl=LLM_SERVER_URL,model_name=MODEL_NAME, temperature=MODEL_TEMPERATURE):
    if LLM_SERVER_TYPE == "openai":
        import openai 

        from langchain.chat_models import ChatOpenAI
        openai.api_base = llmServerUrl
        apikey = os.environ.get("OPENAI_API_KEY","dumyapikey")

        #chat_model = OpenAI(openai_api_key=apikey, temperature=temperature)
        chat_model = ChatOpenAI(openai_api_key=apikey, model=MODEL_NAME, temperature=MODEL_TEMPERATURE)

        return chat_model 
    else:
      
        chat_model = ChatOllama(base_url=llmServerUrl,
                                model=model_name,
                                # temperature=MODEL_TEMPERATURE,
                                temperature=temperature,
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

def ask_llm_question(llm,question):
    return llm.predict(question)

def getCompressQA():
    promptTemplate = getPromptTemplate()
    model = getModel()
    vectorstore = getVectorDB()
    
    compressor = LLMChainExtractor.from_llm(model)
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=vectorstore.as_retriever())

    # filter = LLMChainFilter.from_llm(model)
    # compression_retriever = ContextualCompressionRetriever(base_compressor=filter, base_retriever=vectorstore.as_retriever())
    return RetrievalQA.from_chain_type(
        model,
        # retriever=vectorstore.as_retriever(),
        retriever=compression_retriever,
        # retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 8}),
#        retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": promptTemplate },
    )

    pass

