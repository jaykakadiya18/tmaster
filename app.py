from flask import (flash, Flask, redirect, render_template, request,
                   session, url_for, send_file, jsonify)

import concurrent.futures
from werkzeug.utils import secure_filename
import os
import datetime
import requests
import time
import json
import pandas as pd

IPROYAL_USER = os.environ.get('IPROYAL_USER')
IPROYAL_PASS = os.environ.get('IPROYAL_PW')

# ips proxy settings
ips = {
    'http': f'http://geo.iproyal.com:12321:{IPROYAL_USER}:{IPROYAL_PASS}'
}

app = Flask(__name__)
app.config["output_li"] = []

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

# SqlAlchemy Database Configuration With Mysql
app.config["SECRET_KEY"] = "sdfsf65416534sdfsdf4653"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
secure_type = "http"

def make_ticket_request(url, event):
    try:
        querystring = {
            "show":"listpricerange",
            "by":"offers inventoryTypes accessibility section",
            "apikey":"b462oi7fic6pehcdkzony5bxhe",
            "apisecret":"pquzpfrfz7zd2ylvtz3w5dtyse"
            }
        payload = ""
        headers = {
            'User-Agent': "user-agent=Mozilla/5.0 (Linux; Android 11; 10011886A Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Safari/537.36",
            'Accept': "*/*",
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate, br",
            'TMPS-Correlation-Id': "4c6c3d21-840b-455f-a499-eacf967ae948",
            'Origin': "https://www.ticketmaster.com",
            'Connection': "keep-alive",
            'Referer': "https://www.ticketmaster.com/",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-site",
            'If-Modified-Since': "Tue, 14 Jun 2022 04:09:45 GMT",
            'If-None-Match': 'W/"006e0bc54a443a39eaf1c15ede4e46e08"',
            'TE': "trailers"
            }
        flag = True
        while flag:
            response = requests.request("GET", url, proxies= ips, headers=headers, data=payload, params=querystring)
            response_text =  json.loads(response.text)
            meta_value = response_text.get("title", "nothing")
            if meta_value!="403 Internal Error" and meta_value!="It's not you - it's us":
                app.config["output_li"].append(response_text)
                print(response_text)
                flag=False

    except Exception as e:
        print(e)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_text_file(file_path):
    try:
      file_path_new = os.path.abspath("result.json")
      os.remove(file_path_new)
    except:
       pass

    

    return "complate"


@app.route("/ticketmaster", methods=["GET", "POST"])
def ticketmaster():
    try:
        input_data = request.files['file']
        path = app.config["UPLOAD_FOLDER"]
        app.config["output_li"] = []

        delete_text_file("result.json")
        delete_text_file("/static/uploads/event_id.csv")
        delete_text_file("event_id.csv")

        if 'file' not in request.files:
            flash('No file part')
            redirect(url_for('home_file', _external=True, _scheme=secure_type))

        if input_data.filename == '':
            flash('No resume selected for uploading')
            redirect(url_for('home_file', _external=True, _scheme=secure_type))

        exten = ""
        if input_data and allowed_file(input_data.filename):
            filename = secure_filename(input_data.filename)
            exten = filename.split(".")[-1]
            input_data.save(filename)
            input_data_path = filename

            session["input_data_path"] = input_data_path
        else:
            flash('This file format is not supported.....')
            redirect(url_for('home', _external=True, _scheme=secure_type))

        if exten:
            if exten=="csv":
                df = pd.read_csv(session["input_data_path"], header=None, skiprows=1, names=["event_id"])
            else:
                df = pd.read_excel(session["input_data_path"], header=None, skiprows=1, names=["event_id"])

        worker_length = int(df.shape[0]/1)
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=worker_length)
        
        threads = []

        start_time = time.time()
        data = list(df["event_id"])

        for ev in data:
            url = f"https://offeradapter.ticketmaster.com/api/ismds/event/{ev}/facets"
            threads.append(executor.submit(make_ticket_request, url, ev))

        concurrent.futures.wait(threads)

        json_data = app.config["output_li"]
        with open("result.json", "w") as json_file_dump:
            json.dump(json_data, json_file_dump)
        print(f"total time {time.time()-start_time}")

        message = f"Process Completed. Please download your output file using Download button\nTime taken for that process {time.time()-start_time}"

        return {"message": message, "response":json_data}


    except Exception as e:
        print(e)
        message = "Server Not Responding"
        return jsonify(message=message)



@app.route("/", methods=["GET", "POST"])
def home():
    try:
        return render_template("index.html")

    except Exception as e:
        print(e)
        return render_template("index.html")

@app.route("/download_logs", methods=['GET'])
def download_logs():
    file = os.path.abspath("result.json")
    return send_file(file, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)


#where is ip creds
#Time should be less than 30 secs