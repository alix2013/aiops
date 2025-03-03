import slack_sdk
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode import SocketModeClient

import logging
# import json
import os
from dotenv import load_dotenv
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO)
load_dotenv(dotenv_path="slack.env")
logging.info(f"API_SERVER_URL:{os.environ.get('API_SERVER_URL')}")
from apiclient import askAI

token =  str(os.environ.get('SLACK_TOKEN')) 
app_level_token= str(os.environ.get('SLACK_APP_TOKEN'))   
user_id=str(os.environ.get("SLACK_USER_ID"))  

logging.info(f"userID:{user_id}, token:{token}, app_level_token:{app_level_token}")

# Initialize a new SocketModeClient instance
client = SocketModeClient(
    app_token=app_level_token,
    web_client=slack_sdk.WebClient(token=token)
)

# processed_messages
processed_messages = set()

# Define a function to handle "message" events
def handle_message(client: SocketModeClient, req: SocketModeRequest):
    try:
        if req.type == "events_api":
            event = req.payload["event"]
            logging.info(f"Slack event data:{event}")
            # print("Event data: ", event)
            if event["type"] == "message" and user_id in event["text"]:
                # handel duplicated message
                if event["ts"] in processed_messages:
                    logging.info(f"Duplicate message ignored:{event['ts']}")
                    return
                # Add the message's ts to the set of processed messages
                processed_messages.add(event["ts"])

                channel_id = event["channel"]
                # get received message without userid info
                message = event["text"].replace(f"<@{user_id}>","")
                answer = askAI(message) 
                logging.info(f"Response from APIServer:{answer}")

                # send message back to channel
                client.web_client.chat_postMessage(
                    channel=channel_id,
                    text=str(answer["response"]) + f"<@{event['user']}>"
                )
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)
    except slack_sdk.errors.SlackApiError as e:
      print(f"Error sending message: {e.response['error']}")
    except Exception as e:
      print(f"An unexpected error occurred: {str(e)}")

# Add the event handler to the SocketModeClient
client.socket_mode_request_listeners.append(handle_message)

import time
# Start the SocketModeClient
client.connect()

while True:
    time.sleep(2)
    print("Sleep...")

