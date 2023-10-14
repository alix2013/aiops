from flask_cors import CORS
import os
import logging
from flask import Flask, jsonify, request

from base import ask 

app = Flask(__name__)
CORS(app)

cache = {}

@app.route("/ask", methods=["POST"])
def askAI():
    # global QA

    # user_prompt = request.form.get("user_prompt")
    request_data = request.get_json()
    # print("request_json:", request_data)
    user_prompt = request_data.get("request")


    if user_prompt:
        # return from simple cache
        if user_prompt in cache:
            prompt_response_dict = cache[user_prompt]
            print("return from cache")
            return jsonify(prompt_response_dict), 200

        # print(f'User Prompt: {user_prompt}')
        # Get the answer from the chain
        res = ask(user_prompt)
        answer, docs = res["result"], res["source_documents"]

        prompt_response_dict = {
            "request": user_prompt,
            "response": answer,
        }

        prompt_response_dict["Sources"] = []
        for document in docs:
            prompt_response_dict["Sources"].append(
                (os.path.basename(str(document.metadata["source"])), str(document.page_content))
            )
        # response = jsonify(prompt_response_dict)
        # print(json.dumps(response))
        print(prompt_response_dict)
        cache[user_prompt] = prompt_response_dict

        return jsonify(prompt_response_dict), 200
        # return response, 200
    else:
        return "No user prompt received", 400

@app.route("/ask4pd", methods=["POST"])
def askAI4pd():
    # global QA

    # user_prompt = request.form.get("user_prompt")
    request_data = request.get_json()
    # print("request_json:", request_data)
    user_prompt = request_data.get("request")
    if user_prompt:
        # return from simple cache
        if user_prompt in cache:
            prompt_response_dict = cache[user_prompt]
            print("return from cache")
            return jsonify(prompt_response_dict), 200

        # print(f'User Prompt: {user_prompt}')
        # Get the answer from the chain
        prompt_prefix = "Hi, I get the following information, please give some advice about how to troubleshoot the problem: "
        new_user_prompt = prompt_prefix + user_prompt

        res = ask(user_prompt)
        answer, docs = res["result"], res["source_documents"]

        prompt_response_dict = {
            "request": user_prompt,
            "response": answer,
        }

        prompt_response_dict["Sources"] = []
        for document in docs:
            prompt_response_dict["Sources"].append(
                (os.path.basename(str(document.metadata["source"])), str(document.page_content))
            )
        # response = jsonify(prompt_response_dict)
        # print(json.dumps(response))
        print(prompt_response_dict)
        cache[user_prompt] = prompt_response_dict

        return jsonify(prompt_response_dict), 200
        # return response, 200
    else:
        return "No user prompt received", 400

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    app.run(debug=False, port=5001, host="0.0.0.0")


