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
    pass

@app.route("/", methods=["POST", "GET"])
def addToCsv():
    pass

if __name__=='__main__': 
   app.run(host="0.0.0.0", port=os.getenv("PORT", 3000), debug=True)