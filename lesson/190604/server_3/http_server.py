from flask_restful import Resource, Api
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
 
@app.route('/about')
def about():
  return render_template('about.html')

app.run(host='0.0.0.0', port=8080, debug=True)
