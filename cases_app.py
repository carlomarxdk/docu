from flask import Flask, render_template, request, url_for, redirect
import sqlite3 as sql


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
        return redirect(url_for("output", case_id = case_id))
    return render_template("cases.html",rows = cases)

@app.route('/output')
def output():
    value = request.args.get('case_id', None)
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * from CASES WHERE ID IS %s" %value )
    case = cur.fetchall()[0];
    cur.execute("SELECT * from DOCUMENTS WHERE CASE_ID IS %s" %value )
    documents = cur.fetchall();
    return render_template("output.html", case_info  = case, documents = documents )
if __name__ == '__main__':
   app.run(debug = True)