import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for, current_app, Response, jsonify
from crowlib import Status, load_csv, save_csv, log, LogType

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    filename = request.args.get("filename", "default", type=str)
    value_list = [ # a temporary test list
        {
            "a": "abc",
            "b": "def",
            "c": "ghi"
        },
        {
            "a": "123",
            "b": "456",
            "c": "789"
        }
    ]
    input_list = list(value_list[0].keys())
    return render_template("entry.html", filename=filename, input_list=input_list, value_list=value_list)

@app.route("/add", methods=["POST", "GET"])
def addToCsv():
    return render_template("base.html")

if __name__=='__main__': 
   app.run(host="0.0.0.0", port=os.getenv("PORT", 3000), debug=True)