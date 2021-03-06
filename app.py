from flask import Flask, render_template, request, url_for, redirect, current_app
import sqlite3 as sql
import pdb
import uuid
import datetime
from werkzeug.utils import secure_filename
import os

### NOTIFICATIONS
import email
import smtplib


DATABASE = 'database/data.db'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('.cases'))
    return render_template('login.html')

@app.route('/cases', methods = ['GET', 'POST'])
def cases():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM CASES")
    cases = cur.fetchall();
    if request.method == "POST":
        case_id = request.form.get("case_id")
        return redirect(url_for(".output", case_id = case_id))
    return render_template("cases.html",rows = cases)

@app.route('/output', methods = ['GET', 'POST'])
def output():
    value = request.args.get('case_id')

    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * from CASES WHERE ID IS %s" %value)
    case_info = cur.fetchall()[0];
    cur.execute("SELECT * from DOCUMENTS WHERE CASE_ID IS %s" %value)
    documents = cur.fetchall();  
    
    status = {}
    for document in documents:
        cur.execute("SELECT * FROM APPROVALS WHERE DOC_ID = '%s' ORDER BY id DESC LIMIT 0 , 1 " %document["ID"])
        status[document["ID"]] = cur.fetchall()[0]["STATUS"]

    if request.method == "POST":
        case_id = request.form.get("case_id", None)
        approvals = case_id = int(request.form.get("selection"))
        for document in documents:
            file_id = document["ID"]
            appr = request.form.get(file_id)
            file_type = document["TYPE"]
            file_appr = document["RESPONSIBLE"]
            #if appr != "":
            #    pattern = """INSERT INTO approvals( type, doc_id, status, datetime, responsible) VALUES(?, ?, ?, ?, ?);"""
            #    cur.execute(pattern, (file_type, file_id, appr,  datetime.datetime.now(), str(file_appr)))
            #    con.commit()


        #return redirect(url_for("output", case_id = n))
        return redirect(url_for("add"), case_id = case_id, appr = appr)
    return render_template("output.html", case_info  = case_info, documents = documents, dir = current_app.root_path, status = status)


@app.route('/add', methods = ['GET', 'POST'])
def add():
    case_id = request.args.get('case_id')
    appr = request.args.get('appr')
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * from USERS" )
    users = cur.fetchall();
    if request.method == "POST":
        ## Collect data from the form
        case_id = int(request.form.get("case_id"))
        file_name = request.form.get("file_name")
        file_desc = request.form.get("file_description")
        file_type = request.form.get("file_type")
        file_appr = request.form.get("users")
        file_id = str(uuid.uuid4()).replace("-", "")
        file = request.form.get("file")
        file_datetime = datetime.datetime.now()
        file = request.files['file']
        format = file.filename.split(".")[-1]
        file_path = os.path.join(current_app.root_path, "docs", secure_filename(file_id + "." + format))

        ## Insert into the database
        con = sql.connect(DATABASE)
        cur = con.cursor()
        pattern = """INSERT INTO documents(id, type, description, case_id, responsible, creation_date, file_path) VALUES(?, ?, ?, ?, ?, ?, ?);"""
        cur.execute(pattern, (file_id, file_type, file_desc, case_id, str(file_appr), file_datetime, file_path))
        con.commit()
        pattern = """INSERT INTO approvals( type, doc_id, status, datetime, responsible) VALUES(?, ?, ?, ?, ?);"""
        cur.execute(pattern, (file_type, file_id, "PENDING",  datetime.datetime.now(), str(file_appr)))
        con.commit()
        ### FILE UPLOAD
        file.save(os.path.join("docs", secure_filename(file_id + "." + format)))

        ## Data for the OUTPUT.HTML
        #return render_template("new_document.html", users = users, case_id = case_id)
        #return render_template("output.html", case_info  = case_info, documents = documents)
        return redirect(url_for(".output", case_id = case_id))
    return render_template("new_document.html", users = users, case_id = case_id, appr=appr)



if __name__ == '__main__':
   app.run(debug = True)