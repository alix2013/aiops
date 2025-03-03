import gradio as gr
from llmbase import getQA 
from dotenv import load_dotenv
import os
from actiontool import checkIfAction,runAction

if not load_dotenv():
    print("Load .env file failed . Please check if it exists")
    exit(1)

CHAT_UI_TITLE = os.environ.get("CHAT_UI_TITLE","AI Assistant")
CHAT_UI_INPUT_PLACEHOLDER=os.environ.get("CHAT_UI_INPUT_PLACEHOLDER","Ask me question")
CHAT_UI_PORT=os.environ.get("CHAT_UI_PORT","5005")

# QA = getQA(useHistory=True)
QA = getQA()

def format_chat_prompt(message, chat_history, max_length):
    prompt = ""
    for turn in chat_history[-max_length:]:
        user_message, bot_message = turn
        prompt = f"{prompt}\nUser: {user_message}\nAssistant: {bot_message}"
    prompt = f"Here are conversation history:\n{prompt}"  
    prompt = f"{prompt}\nUser: {message}\nAssistant:"
    return prompt


def ask(question, history):
    # isAction, act = checkIfAction(question)
    # if ( isAction == True ):
    #     print(f"run action: {act}" )
    #     answer = runAction(question)
    #     return answer
    prompt = format_chat_prompt(question,history, 50)
    # res = QA({"query": question})
    # print("--->",prompt)
    res = QA({"query": prompt})
    answer, sourceDocs = res["result"], res["source_documents"]
    retMsg = f"{answer}\n"
    # retMsg = f"{answer}\n---\n***HERE ARE REFERENCED SOURCE DOCUMENTS***\n "
    # for i, document in enumerate(sourceDocs):
    #   source = os.path.basename(str(document.metadata['source'])) 
    #   retMsg = retMsg + f"{i+1}.{source}:\n```{document.page_content}\n```\n "
    print(f"Question: {question}\nAnswer: {answer}")
    print("-"*80)
    return retMsg

if __name__ == "__main__":
    gr.ChatInterface(
        ask,
        theme=gr.themes.Soft(),
        chatbot=gr.Chatbot(show_copy_button=True, value=[[None, "Hi, this is FusionBot, How can I help you today?"]]),
        textbox=gr.Textbox(lines=1,placeholder=CHAT_UI_INPUT_PLACEHOLDER,  scale=10),
        title=CHAT_UI_TITLE,
        # description="Ask any question about Fusion/Kubernetes",
        # examples=["Hello", "How to create POD?" ],
        # cache_examples=True,
        retry_btn=None,
        # undo_btn="Delete Previous",
        # clear_btn="Clear",
        undo_btn=None,
        clear_btn="Clear",
        css="footer {visibility: hidden}"
    ).launch(server_port=int(CHAT_UI_PORT), server_name="0.0.0.0")


