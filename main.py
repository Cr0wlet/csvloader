import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for, current_app, Response, jsonify
from crowlib import tidy_filename, tidy_text, load_csv, save_csv, make_entity, log, LogType
from markupsafe import escape

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        filename = tidy_filename(request.args.get("filename", "default"))
        value_list = load_csv(filename)
        input_list = []
        if not len(value_list) == 0:
            log(LogType.DEBUG, "Line 20: in home() > if not len(value_list) == 0 ...", value_list)
            input_list = list(value_list[0].keys())
            return render_template("entry.html", filename=filename, input_list=input_list, value_list=value_list)
        else: # file doesn't exist or doesn't have values, so have user make new csv at "/new"
            return redirect(f"/new?filename={filename}")
    elif request.method == "POST": # ...just came back from "/new", and passing headings by POST from "/new"
        filename = tidy_filename(request.form.get("filename", "default"))
        value_list = []
        input_list = []
        for k, v in request.form.items(): # get headers for new csv file
            if not k == 'filename':
                input_list.append(tidy_text(v))
        if not len(input_list) == 0: # if there are headers/columns, then go to entry form
            return render_template("entry.html", filename=filename, input_list=input_list, value_list=value_list)
        else: # ...otherwise, go back to define columns
            return redirect(f"/new?filename={filename}&message=Please+enter+a+column+name.")

@app.route("/new", methods=["GET"])
def create_new_csv():
        filename = tidy_filename(request.args.get("filename", ""))
        return render_template("new.html", filename=filename)

@app.route("/add", methods=["POST"])
def add_to_csv():
    filename = "default"
    data = {}
    for x in request.form.keys(): # 1.b. get values from form, using `request.form.keys()` (the column names)
        log(LogType.DEBUG, f"x={x}, data[x]={request.form.get(x, "")}")
        if x == "filename":
            filename = request.form.get(x, "default") # 1.b. and get the filename
        else:
            data[x] = tidy_text(request.form.get(x, ""))
    value_list = load_csv(filename) # 2. get previous item values from `filename`.csv
    value_list.append(data) # 4. add to list
    log(LogType.DEBUG, f"value_list={value_list}")
    save_csv(value_list, filename) # 5. save
    return redirect(f"/?filename={filename}")

if __name__=='__main__': 
   app.run(host="0.0.0.0", port=os.getenv("PORT", 3000), debug=True)