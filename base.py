from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import torch
import os 
from dotenv import load_dotenv
import logging

# device_type="mps"
device_type="cuda" if torch.cuda.is_available() else "cpu"
if not load_dotenv():
    print("Load .env file failed . Please check if it exists")
    exit(1)

EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL_NAME","hkunlp/instructor-large")
DB_DIRECTORY = os.environ.get('DB_DIRECTORY', "./DB")
MODEL_NAME = os.environ.get('MODEL_NAME',"mistral")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
)


logging.info(f"MODEL_NAME: {MODEL_NAME}")
logging.info(f"DB_DIRECTORY: {DB_DIRECTORY}")
logging.info(f"EMBEDDING_MODEL_NAME: {EMBEDDING_MODEL_NAME}")


embeddings = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": device_type})
vectorstore = Chroma(
    persist_directory=DB_DIRECTORY,
    embedding_function=embeddings,
)

def getPromptTemplate():
    template = """[INST] <<SYS>> Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible. <</SYS>>
    {context}
    Question: {question}
    Helpful Answer:[/INST]"""
    promptTemplate = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )
    return promptTemplate


def getModel(llmServerUrl="http://localhost:11434",model_name=MODEL_NAME):
    chat_model = ChatOllama(base_url=llmServerUrl,
                            model=model_name,
                            verbose=True,
                            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    return chat_model 


promptTemplate = getPromptTemplate()
chat_model = getModel()
QA = RetrievalQA.from_chain_type(
    chat_model,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": promptTemplate},
)

def ask(question):
    global QA

    result = QA({"query": question})
    return result
