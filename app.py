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
        type = request.form.get("type")
        file_name = request.form.get("file_name")
        file_appr = request.form.get("type")
        con = sql.connect(DATABASE)
        #con.row_factory = sql.Row
        cur = con.cursor()
        pattern = """INSERT INTO documents(description, type) VALUES(?, ?);"""
        cur.execute(pattern, (file_appr, file_name))
        con.commit()
        return render_template("new_document.html", users = users, case_id = case_id, res = type)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

    return render_template("new_document.html", users = users, case_id = case_id, res = None)
if __name__ == '__main__':
   app.run(debug = True)