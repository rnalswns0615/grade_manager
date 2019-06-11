from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def __init__(self):
        pass
    def post(self):
        #return {"message" : "ok", "code": "200", "results" : "Test."}
        return {"인사":"환영합니다."}


api.add_resource(Test, '/test')

if __name__== '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

