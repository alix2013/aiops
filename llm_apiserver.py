from flask_cors import CORS
import os
import logging
from flask import Flask, jsonify, request
from base import getQA

app = Flask(__name__)
CORS(app)
cache = {}

QA = getQA()
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
        return "No user prompt received", 400

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
        return "No user prompt received", 400

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    app.run(debug=False, port=int(os.environ.get("PORT","5001")), host="0.0.0.0")


