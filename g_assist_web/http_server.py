from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from sm_helper import StudentManager
 
app = Flask(__name__)
api = Api(app)

sm = StudentManager()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result_1',methods = ['POST'])
def result_1():
    if request.method == 'POST':
        sm = StudentManager()
        result = request.form
        st_name = result['st_name']
        st_class = result['st_class']
        print ("st_name : {}, st_class : {}".format(st_name, st_class))
        result_dic = sm.view_student_grade(st_class, st_name)
        #result = {'result' : result_dic}
        return render_template("result_1.html",result = result_dic)

@app.route('/result_2',methods = ['POST'])
def result_2():
    if request.method == 'POST':
        sm = StudentManager()
        result_dic = sm.view_class_grade()
        #result = {'result' : result_dic}
        return render_template("result_2.html",result = result_dic)

@app.route('/result_3',methods = ['POST'])
def result_3():
    if request.method == 'POST':
        sm = StudentManager()
        result = request.form
        st_name = result['st_name']
        st_class = result['st_class']
        g_math = result['g_math']
        g_english = result['g_english']
        g_korean = result['g_korean']
        g_physics = result['g_physics']
        g_alchemy = result['g_alchemy']
        result_str = sm.write_grade(st_class, st_name, g_math, g_english, g_korean, g_physics, g_alchemy)
        #result = {'result' : result_dic}
        result = {'result':result_str}
        return render_template("result_1.html",result = result)
"""
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


api.add_resource(View_Stgrade, '/view_stgrade')
api.add_resource(Insert_Student, '/insert_student')
api.add_resource(View_Classgrade, '/view_classgrade')
"""

if __name__== '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

