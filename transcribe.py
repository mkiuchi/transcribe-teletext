import os
import sys
import json
from datetime import datetime, timedelta
import argparse

parser = argparse.ArgumentParser()
g1 = parser.add_argument_group("transcribed file")
g1.add_argument("-f", "--file",
                  required=True,
                  help="input transcribed json file",
                  type=str)
g2 = parser.add_mutually_exclusive_group(required=True)
g2.add_argument("-r", "--realtime",
                  help="output realtime as teletext",
                  action="store_true")
g2.add_argument("-d", "--dump",
                  help="dump whole output",
                  action="store_true")

def readTranscribe(filename):
    with open(filename) as fh:
        try:
            jsonobj = json.load(fh)
        except:
            raise
    return jsonobj

def teletext(jsonobj):
    print("--- START TELETEXT ---")
    idx = int(0)
    ntime = float(0.0)
    jsonlength = len(jsonobj)
    n1 = datetime.now()
    while True:
        if "start_time" in jsonobj[idx]:
            #print(float(jsonobj[idx]["start_time"]), ntime)
            if float(jsonobj[idx]["start_time"]) < ntime:
                print(jsonobj[idx]["alternatives"][0]["content"], end=' ')
                idx += 1
                if idx >= jsonlength:
                    break
        else:
            if jsonobj[idx]["alternatives"][0]["content"] == ',':
                print(chr(0x08)+jsonobj[idx]["alternatives"][0]["content"], end=' ')
            else:
                print(chr(0x08)+jsonobj[idx]["alternatives"][0]["content"])
            idx += 1
            if idx >= jsonlength:
                break
        d = datetime.now() - n1
        ntime = float(d.total_seconds())
    print("--- END OF TELETEXT ---")

def dumpTranscribe(jsonobj):
    idx = int(0)
    jsonlength = len(jsonobj)
    while True:
        if "start_time" in jsonobj[idx]:
            #print(float(jsonobj[idx]["start_time"]), ntime)
            print(jsonobj[idx]["alternatives"][0]["content"], end=' ')
            idx += 1
            if idx >= jsonlength:
                break
        else:
            if jsonobj[idx]["alternatives"][0]["content"] == ',':
                print(chr(0x08)+jsonobj[idx]["alternatives"][0]["content"], end=' ')
            else:
                print(chr(0x08)+jsonobj[idx]["alternatives"][0]["content"])
            idx += 1
            if idx >= jsonlength:
                break

jsonobj = None

args = parser.parse_args()
if args.dump:
    dumpTranscribe(readTranscribe(args.file)["results"]["items"])
elif args.realtime:
    teletext(readTranscribe(args.file)["results"]["items"])
else:
    raise("-r or -d should be set")
