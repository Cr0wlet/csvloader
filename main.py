import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for, current_app, Response, jsonify
from crowlib import Status, load_csv, save_csv, make_entity, log, LogType

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    filename = request.args.get("filename", "default")
    value_list = load_csv(filename)
    input_list = list(value_list[0].keys())
    return render_template("entry.html", filename=filename, input_list=input_list, value_list=value_list)

@app.route("/add", methods=["POST"])
def addToCsv():
    filename = "default"
    data = {}
    for x in request.form.keys():
        if x == "filename":
            filename = request.form.get(x, "default")
        else:
            data[x] = request.form.get(x, "")
    input_list = list(value_list[0].keys()) # 1a. get header values
    value_list = load_csv(filename) # 1b. and get previous item values from `filename`.csv
    entity = make_entity(input_list, [data]) # 2. make a new entry/entity
    value_list.append(entity) # 3. add to list
    save_csv(value_list, filename) # 4. save
    return render_template("entry.html", filename=filename, input_list=input_list, value_list=value_list)

if __name__=='__main__': 
   app.run(host="0.0.0.0", port=os.getenv("PORT", 3000), debug=True)