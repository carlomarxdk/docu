from flask import Flask, render_template
import sqlite3 as sql


DATABASE = 'database/data.db'

app = Flask(__name__)

@app.route('/')
def get_users():
   con = sql.connect(DATABASE)
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from people")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)




if __name__ == '__main__':
   app.run(debug = True)