from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/up', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       file = request.files['file']
       filename = secure_filename(file.filename)
       file.save(secure_filename(file.filename))
       return 'file uploaded successfully'
