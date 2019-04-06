# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 20:51:34 2019
확인하기위한 패스
@author: 구상수
"""
import operator
from random import *


class StudentManager:
    def __init__(self):
        pass

    @staticmethod
    def get_ranking(st_name, grade_dic):
        sorted_dic = sorted(grade_dic.items(), key=operator.itemgetter(1),reverse=True)
        dic_keys= dict(sorted_dic).keys()
        for i, dic_key in enumerate(dic_keys):
            if st_name == dic_key:
                count = i + 1
                break
        return count



    def view_grade_old(self, name):
        f =  open("C:/Users/구상수/.spyder-py3/study/grade.txt", 'r')
        lines = f.readlines()
        for line in lines:

            if line.find(name) >= 0:
                print(line.split(':')[1])
    @staticmethod
    def view_grade(name):
        avg = {}
        math = {}
        english = {}
        korean = {}
        physics = {}
        alchemy = {}

        f =  open("C:/Users/구상수/.spyder-py3/study/grade.txt", 'r')
        lines = f.readlines()
        total = len(lines)

        for line in lines:
            student = line.split(':')[0]
            all_grade = line.split(':')[1].split('\t')
            sum = 0
            for x in all_grade:
                sum = sum + int(x)
            avg[student] = sum / len(all_grade)
            math[student] = int(all_grade[0])
            english[student] = int(all_grade[1])
            korean[student] = int(all_grade[2])
            physics[student] = int(all_grade[3])
            alchemy[student] = int(all_grade[4])
        grade_report = {}
        grade_report['avg'] = [avg[name],
                             StudentManager.get_ranking(name, avg),
                             round(StudentManager.get_ranking(name, avg) / total * 100, 2)]
        grade_report['math'] = [math[name],
                             StudentManager.get_ranking(name, math),
                             round(StudentManager.get_ranking(name, math) / total * 100, 2)]
        grade_report['english'] = [english[name],
                             StudentManager.get_ranking(name, english),
                             round(StudentManager.get_ranking(name, english) / total * 100, 2)]
        grade_report['korean'] = [korean[name],
                             StudentManager.get_ranking(name, korean),
                             round(StudentManager.get_ranking(name, korean) / total * 100, 2)]
        grade_report['physics'] = [physics[name],
                             StudentManager.get_ranking(name, physics),
                             round(StudentManager.get_ranking(name, physics) / total * 100, 2)]
        grade_report['alchemy'] = [alchemy[name],
                             StudentManager.get_ranking(name, alchemy),
                             round(StudentManager.get_ranking(name, alchemy) / total * 100, 2)]
        print(grade_report)




    def write_grade(self, name, math, english, korean, physics, alchemy):
        f =  open("C:/Users/구상수/.spyder-py3/study/grade.txt", 'a')
        student = '{}:{}\t{}\t{}\t{}\t{}'.format(
                    name,
                    math,
                    english,
                    korean,
                    physics,
                    alchemy
                    )
        print(student)
        f.write('\n')
        f.write(student)
        f.close()

#    @staticmethod
#    def write_rd_grade(loop):
#


if __name__ == '__main__':
    sm = StudentManager()
    sm.view_grade("김민석")
#    sm.write_grade("김성재", '99', '45', '4', '0', '0')
    sm.view_grade("김승재")
    sm.view_grade("김성재")
