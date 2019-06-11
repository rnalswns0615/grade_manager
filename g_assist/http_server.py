from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sm_helper import StudentManager
 
app = Flask(__name__)
api = Api(app)

sm = StudentManager()
class View_Stgrade(Resource):
    def __init__(self):
        pass
    def post(self):
        st_name = request.json['st_name']
        st_class = request.json['st_class']
        print ("st_name : {}, st_class : {}".format(st_name, st_class))
        result_dic = sm.view_student_grade(st_class, st_name)
        #return {"message" : "ok", "code": "200", "results" : "Test."}
        #return {"이름":st_name, "반":st_class}
        return {'result' : result_dic}


class Insert_Student(Resource):
    def __init__(self):
        pass
    def post(self):
        st_name = request.json['st_name']
        st_class = request.json['st_class']
        g_math = request.json['g_math']
        g_english = request.json['g_english']
        g_korean = request.json['g_korean']
        g_physics = request.json['g_physics']
        g_alchemy = request.json['g_alchemy']
       
        print ("st_name : {}, st_class : {}, score : {}|{}|{}|{}|{}".format(
            st_name,
            st_class,
            g_math,
            g_english,
            g_korean,
            g_physics,
            g_alchemy))
        # print ("st_name : {}, st_class : {}".format(st_name, st_class))
        insert_result = sm.write_grade(st_class,
                                    st_name,
                                    g_math,
                                    g_english,
                                    g_korean,
                                    g_physics,
                                    g_alchemy)
        #return {"message" : "ok", "code": "200", "results" : "Test."}
        #return {"이름":st_name, "반":st_class}
        return {'result' : insert_result}


class View_Classgrade(Resource):
    def __init__(self):
        pass
    def post(self):
        result_dic = sm.view_class_grade()
        #return {"message" : "ok", "code": "200", "results" : "Test."}
        #return {"이름":st_name, "반":st_class}
        return {'result' : result_dic}


if __name__== '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

