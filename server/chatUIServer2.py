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

QA = getQA()

def ask(question, history=""):
    isAction, act = checkIfAction(question)
    if ( isAction == True ):
        print(f"run action: {act}" )
        answer = runAction(question)
        return answer

    res = QA({"query": question})
    answer, sourceDocs = res["result"], res["source_documents"]
    retMsg = f"{answer}"
    # retMsg = f"{answer}\n---\n***HERE ARE REFERENCED SOURCE DOCUMENTS***\n "
    # for i, document in enumerate(sourceDocs):
    #   source = os.path.basename(str(document.metadata['source'])) 
    #   retMsg = retMsg + f"{i+1}.{source}:\n```{document.page_content}\n```\n "
    return retMsg


def format_chat_prompt(message, chat_history, max_convo_length):
    prompt = ""
    for turn in chat_history[-max_convo_length:]:
        user_message, bot_message = turn
        prompt = f"{prompt}\nUser: {user_message}\nAssistant: {bot_message}"
    prompt = f"Here are conversation history:\n{prompt}"  
    prompt = f"{prompt}\nUser: {message}\nAssistant:"
    return prompt

def respond(message, chat_history, max_convo_length = 50):
        formatted_prompt = format_chat_prompt(message, chat_history, max_convo_length)
        print(f"--->{formatted_prompt}")
        # bot_message = chat(system_prompt = 'You are a friendly chatbot. Generate the output for only the Assistant.',
        #                    user_prompt = formatted_prompt)
        bot_message = ask(formatted_prompt)
        chat_history.append((message, bot_message))
        return "", chat_history

if __name__ == "__main__":
    # gr.ChatInterface(
    #     # ask,
    #     askAI,
    #     theme=gr.themes.Soft(),
    #     chatbot=gr.Chatbot(show_copy_button=True ),
    #     textbox=gr.Textbox(lines=1,placeholder=CHAT_UI_INPUT_PLACEHOLDER,  scale=10),
    #     title=CHAT_UI_TITLE,
    #     # description="Ask any question about Fusion/Kubernetes",
    #     # examples=["Hello", "How to create POD?" ],
    #     # cache_examples=True,
    #     retry_btn=None,
    #     # undo_btn="Delete Previous",
    #     # clear_btn="Clear",
    #     undo_btn=None,
    #     clear_btn=None,
    #     css="footer {visibility: hidden}"
    # ).launch(server_port=int(CHAT_UI_PORT), server_name="0.0.0.0")


    with gr.Blocks() as demo:
        
        chatbot = gr.Chatbot(height=400,title=CHAT_UI_TITLE) 
        msg = gr.Textbox(label="Input Question")
        btn = gr.Button("Submit")
        clear = gr.ClearButton(components=[msg, chatbot], value="Clear History")

        btn.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
        msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot]) #Press enter to submit
    gr.close_all()
    # demo.launch()
    demo.launch(server_port=int(CHAT_UI_PORT), server_name="0.0.0.0")

