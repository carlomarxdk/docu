from flask import Flask, render_template, request, url_for, redirect
import sqlite3 as sql
import pdb

DATABASE = 'database/data.db'

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def get_overview():
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
    if request.method == "POST":
        case_id = request.form.get("case_id", None)
        #return redirect(url_for("output", case_id = n))
        return redirect(url_for("add"), case_id = case_id)
    return render_template("output.html", case_info  = case_info, documents = documents)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    case_id = request.args.get('case_id')
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
        ## Insert into the database
        con = sql.connect(DATABASE)
        cur = con.cursor()
        pattern = """INSERT INTO documents(type, description, case_id, responsible) VALUES(?, ?, ?, ?);"""
        cur.execute(pattern, (file_type, file_desc, case_id, str(file_appr)))
        con.commit()
        ## Data for the OUTPUT.HTML
        return render_template("new_document.html", users = users, case_id = case_id)
        #return render_template("output.html", case_info  = case_info, documents = documents)
    return render_template("new_document.html", users = users, case_id = case_id)


if __name__ == '__main__':
   app.run(debug = True)