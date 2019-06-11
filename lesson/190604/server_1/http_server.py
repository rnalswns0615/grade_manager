from flask_restful import Resource, Api
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return '''<!DOCTYPE HTML><html>
  <head>
    <title>Flask app</title>
  </head>
  <body>
    <h2>Hello Flask!</h2>
  </body>
</html>'''
 
@app.route('/about')
def about():
    return 'About 페이지'

app.run(host='0.0.0.0',port=8080, debug=True)
