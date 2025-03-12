import datetime
import os, json
import re
import csv
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from marshmallow import Schema, fields, ValidationError, validate, post_load

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

'''
==== CONSTANTS ====
'''
class LogType:
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    WARN = "WARN"

SUCCESS = 0
FAIL = 1

class Status:
    '''Http status codes'''
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503


def log(type: str, message: str, *dump):
    print("[{0}] {1}: {2}{3}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), type, message, f"\n{dump}" if dump else ""))

def tidy_text(value: str) -> str:
    '''Removes extra whitespace in and around text'''
    out = value.strip()
    return out

def tidy_list(lst: list) -> list[str]:
    '''Calls `tidy_text()` on items in list'''
    out = lst
    for x in out:
        out[out.index(x)] = tidy_text(x)
    return out

def make_entity(headers: list, values: list) -> dict:
    entity = {}
    for x in headers:
        entity[x] = values[headers.index(x)]
    return entity

def load_csv(filename: str) -> list:
    '''Loads a csv file'''
    outpath = Path(f"{os.getenv("CSVLOADER_FILE_PATH")}/{filename}.csv")
    outpath.parent.mkdir(exist_ok=True) # make sure the directory the files are in exists
    csvlist = [] # our final product, a list of entities from our csv file
    headers = [] # the columns' headings
    try:
        f = outpath.open("r", newline="")
        reader = csv.reader(f)
        for line in reader:
            tidy_list(line) # remove extra whitespaces and other bad stuff
            if reader.line_num == 1:
                for h in line:
                    headers.append(h) # start collecting headers if this is line 1
            else:
                csvlist.append(make_entity(headers, line)) # add entity to list if this is any other line but line 1
        return csvlist
    except Exception as e:
        log(LogType.ERROR, "There was an error reading the file.", e)
        return []

def save_csv(all_entries: list[dict], out_file: str) -> int:
    '''Accepts a list of all "current" entries (old and new) and saves it as a csv file (`out_file`).'''
    outpath = Path(f"{os.getenv("CSVLOADER_FILE_PATH")}/{out_file}.csv")
    outpath.parent.mkdir(exist_ok=True)
    try:
        f = outpath.open("w", newline="", encoding="utf-8")
        writer = csv.DictWriter(f, delimiter=',', fieldnames=list(all_entries[0].keys())) # get csv writer, with fieldnames taken from the dict keys (converted to list)
        writer.writeheader()
        for row in all_entries:
            writer.writerow(row)
    except Exception as e:
        log(LogType.ERROR, "There was an error while saving the csv.", e)
        return FAIL
    return SUCCESS

def test():
    '''This test runs when `crowlib.py` is the main file to run.'''
    log(LogType.INFO, "Loading 'test.csv'...")
    print(*load_csv("test"), sep="\n")
    test2 = [
        {"a": 1, "b": 2, "c": "three"},
        {"a": 2, "b": 3, "c": "four"},
        {"a": 3, "b": 4, "c": "five"}
    ]
    log(LogType.INFO, "Saving to 'test2.csv'...", test2)
    log(LogType.INFO, "Successfully saved! :)" if not save_csv(test2, "test2") else "Failed to save! :(")

if __name__ == "__main__":
    test()