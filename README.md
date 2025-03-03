# aiops

## Introduction
- 这是一个用于辅助IT技术人员日常运营的AI助理，通过Web browser extension可以  
随时把AI助理呼叫出来，实现和已有的应用程序的无缝集成，用户可以通过在Browser  
选中文字，点右键选择menu Ask AI的子菜单完成和AI的交互，也可以点击extension  
快捷按钮输入文字和AI进行一次性的快速交互，或者通过ChatUI完成就单个主题的多  
轮对话。  
- 此AI助理的API Server提供了简单快捷的RestAPI接口，可以快速接入其他Application，  
如Slack, 微信等任何需要接入AI的第三方应用，调用RestAPI即可。    
- APIServer封装好了常用的Prompt, 方便API client调用，Web Browser extension是  
通过Javascript开发的,没有使用开源框架，API server/ChatServer是使用langchain  
的python SDK开发的. 
- AI助手的知识库部分是通过RAG实现，文档数据向量化后存入VectorDB中。  
- 本AI助手除了有知识问答的功能外，还通过LLM赋予了行为能力，可以帮助用户完成  
对OCP cluster的日常管理，通过配置ACTION_MODEL完成，AI助理不仅会“说”，还会“做”  
具体内容参见Demo视频  
- 除了Browser extension外，本项目有对OCP命令行附加AI的能力，开发了ocAI命令行  
使用方法和oc命令行一样，参见demo视频  
- 本项目完全使用了开源的LLM model,所有服务可部署在本地，也提供了Docker image  
可以部署在OCP cluster上，部署所需要的yaml文件放在openshift目录。  
- 可以通过配置指定和切换不同的开源MODEL，也可以用商用的比如OpenAI的model, 测  
试用的知识库MODEL是mistral 7b的小模型即可， ACTION MODEL对模型要求较高,本项目  
使用了在Mistral基础上fine tuned  neural-chat MODE  

## Architecture
![Architecture](https://github.ibm.com/anlixue/aiops/blob/main/architecture.jpg)


## Main features

- **Open-source Large Language Model Integration**: The project utilizes open-source large language models, offering a cost-effective solution that supports a variety of popular open-source models. This feature allows users to leverage advanced AI capabilities without incurring high costs.

- **Easy Model Switching**: The project provides the flexibility to easily switch between different models by simply modifying environment variables. It also offers seamless transition to commercial models such as OpenAI, providing users with a wide range of options to suit their specific needs.

- **Local Data Storage for Privacy and Compliance**: All data is stored within the local network, minimizing the risk of privacy breaches and ensuring compliance with security regulations. This feature is particularly beneficial for organizations that handle sensitive information.

- **Browser Extension Tool and UI Integration**: The project comes with a browser extension tool and application UI integration. Users can interact with the AI by simply selecting the text, making the usage more convenient and user-friendly.

- **Natural Language Interaction for System Management**: Users can communicate with the system using natural language, allowing the AI to assist in managing clusters, checking the status of various applications, and more. This feature simplifies system management and enhances productivity.

- **Vector Database for Precise AI Feedback**: The project allows users to build a vector database using private, domain-specific documents. This feature enables the AI to provide more accurate and relevant feedback, improving the overall user experience.

- **AI-enhanced Management Tools**: The project enhances management tools like OpenShift OC/Kubectl with AI capabilities. It automatically analyzes data, making troubleshooting easier and more efficient.

- **RestAPI via APIServer**: The APIServer provides RestAPI, making it easier to integrate with various applications. This feature ensures the project's compatibility with a wide range of systems and platforms.

- **Multi-turn Dialogue via ChatServer**: Through the ChatServer, users can engage in multi-turn dialogues with the AI on the same topic. This feature facilitates more in-depth and meaningful interactions with the AI.

## Install chrome extension

- Open the Chrome browser and navigate to chrome://extensions/.
- Enable Developer mode by clicking the toggle switch in the top right corner.
- Click the "Load unpacked" button and select the directory containing your unpacked extension, The extension will now be installed 
- Pin the extension on menu: click the puzzle piece on the top right of your browser. This will open a drop-down of all your Chrome Extensions. From here, simply click the little pin next to the Chrome Extensions
- Right clicked pined icon, choose option, input server URL and chat server URL
- Open chrome, access any page, select text then right click, choose sub-menu item
- Click pined icon to access Q/A, AI action and chat application


## Install server components on Openshift or Kubernetes cluster

### Create pvc 

```shell
oc create -f openshift/apiserver-emmodel-pvc.yaml -f openshift/apiserver-db-pvc.yaml
oc create -f openshift/chatserver-emmodel-pvc.yaml -f openshift/chatserver-db-pvc.yaml

```
### Create deployment, service and route
Edit deployment yaml file env settings, reference the .env example file

```shell

oc create -f openshift/apiserver-deployment.yaml -f openshift/apiserver-service.yaml -f openshift/apiserver-route.yaml
oc create -f openshift/chatserver-deployment.yaml -f openshift/chatserver-service.yaml -f openshift/chatserver-route.yaml

```

## Typical usage examples

- Select some warning/error information on chrome, right click then choose "Ask AI" -> "Ask AI for troubleshooting"
- Select a piece of text on chrome, right click then choose "Ask AI" -> "Ask AI to summarize text"
- Click pined icon of chrome extension, Pop-up a Q/A,action window, input query or action description, or click "chat..." link to access chat UI
- Action description require start with /action:, here are examples action description
    - /action: hi, please list deployment status
    - /action: hi, increase deployment nginx instances to 2
    - /action: hi, please decrease deployment nginx instance number to 1
    - /action: please show me logs of deployment nginx
    - /action:创建一个deployment,名字是webserver, image是ubi9/httpd-24 (Support action description in Chinese)

- ocAI command usage is same as openshift oc command, it adds an AI analysis result at the end of the oc output.

## Build developement environment

### Install python3

### Install requirements
```shell

cd server 
pip install -r requirements.txt 

```

### Configure .env file
Configure .env file or export as system environment variables

```shell

# Large Language Model Server Configuration

LLM_SERVER_URL="http://localhost:12345"
#LLM_SERVER_URL="https://postcard-ut-renew-richardson.trycloudflare.com"

# SERVER_TYPE is openai compatible or not
# LLM_SERVER_TYPE="openai"

#MODEL Name
MODEL_NAME="neural-chat"
#MODEL_NAME="mistral"
#MODEL_NAME="mistral:7b-instruct-q6_K"
#MODEL_NAME="openhermes2-mistral"
#MODEL_NAME="zephyr"
#MODEL_NAME="llama2:7b"
#MODEL_NAME="mistral-openorca"

## MODEL parameter
#MODEL_TEMPERATURE=0
MODEL_TEMPERATURE=0.2

ACTION_MODEL_NAME="neural-chat"
ACTION_MODEL_TEMPERATURE=0

# EMBEDDING_MODEL
EMBEDDING_MODEL_NAME="hkunlp/instructor-large"
#SENTENCE_TRANSFORMERS_HOME="~/.cache/torch/sentence_transformers"

# VECTOR DB Location
DB_DIRECTORY="./DB"
#DB_DIRECTORY="./DB_TSM"

# CHAT UI Configuration
CHAT_UI_TITLE="IBM Storage Fusion AI Assistant"
CHAT_UI_INPUT_PLACEHOLDER="Please ask me questions only for IBM Storage Fusion"
#CHAT_UI_PORT
CHAT_UI_PORT=5006

# Vector DB source directory 
SOURCE_DIRECTORY="./SOURCE_DIRECTORY"

```

