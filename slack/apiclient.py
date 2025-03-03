import requests
import os 
default_apiserver_url="http://localhost:5001"

API_SERVER_URL = os.environ.get("API_SERVER_URL", default_apiserver_url)

def askAI(question, api_url=API_SERVER_URL+"/ask"):
    # api_url =  os.environ.get("API_SERVER_URL",default_apiserver_url)+"/ask"
    headers = {'Content-Type': 'application/json'}
    # JSON payload to be sent in the request body
    payload = {'request': question}

    # Making a POST request with JSON payload
    response = requests.post(api_url, headers=headers, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response in JSON format
        # print(response.json())
        return response.json()
    else:
        # Print an error message if the request was not successful
        # print(f"Error: {response.status_code}")
        # print(response.text)
        return { "errorCode": response.status_code }


if __name__ == "__main__":
    answer = askAI("hello")
    print(answer)

