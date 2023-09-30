
import gradio as gr

import requests
import json
def askAPI(question):
    url = "http://localhost:5001/ask"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data =  {
        "request": question,
    }
    #print("POST data",data)
    resp = requests.post(url, headers=headers, json=data)
    #print(json.dumps(resp.json(), indent=4))
    answer = resp.json().get("response")
    #print(answer)
    return answer

def askAPI4PD(question):
    url = "http://localhost:5001/ask4pd"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data =  {
        "request": question,
    }
    #print("POST data",data)
    resp = requests.post(url, headers=headers, json=data)
    #print(json.dumps(resp.json(), indent=4))
    answer = resp.json().get("response")
    #print(answer)
    return answer

#def askapi(name):
#    return f'Hello {name}!'

iface1 = gr.Interface(fn=askAPI, inputs="text", outputs="text")
iface2 = gr.Interface(fn=askAPI4PD, inputs="text", outputs="text")

# iface1.launch(share=True)
demo = gr.TabbedInterface([iface1, iface2], ["AskAI", "AskAI4PD"])

demo.launch(share=True)





