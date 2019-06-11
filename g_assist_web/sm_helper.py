# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 20:51:34 2019

@author: 구상수
"""
import operator
from random import *


class StudentManager:
    def __init__(self):
        #f =  pen("C:/Users/구상수/.spyder-py3/study/grade.txt", 'r')
        f = open("./grade.txt", 'r')

        lines = f.readlines()
        self._st_lines = lines
    
    @staticmethod
    def get_ranking(st_name, grade_dic):
        sorted_dic = sorted(grade_dic.items(), key=operator.itemgetter(1),reverse=True)
        #print(type(sorted_dic))
        #print(sorted_dic)
        #dic_keys= dict(sorted_dic).keys()
        count = 0
        #for i, dic_key in enumerate(dic_keys):
        for i, dic_key in enumerate(sorted_dic):
            dic_key = dic_key[0]
            #print ('dic_key:'dic_key)
            if st_name == dic_key:
                count = i
                break
        # print ('initial:',count)
        while not(count==0):
            # print ('make : ',count)
            if count != 0 :
                if  sorted_dic[count][1]==sorted_dic[count-1][1]:
                    count -= 1
                else:
                    break    
        return count + 1

    """
    @staticmethod
    def get_ranking(st_name, grade_dic):
        sorted_dic = sorted(grade_dic.items(), key=operator.itemgetter(1),reverse=True)
        #dic_keys= dict(sorted_dic).keys()
        count = 0
        #for i, dic_key in enumerate(dic_keys):
        for i, dic_key in enumerate(sorted_dic):
            dic_key = dic_key[0]
            if st_name == dic_key:
                count = i + 1
                break
        while True:
            
        return count
    """


    def view_grade_old(self, name):
        for line in self.lines:
            if line.find(name) >= 0:
                print(line.split(':')[1])
                
                
    def student_clsranking(self, st_class, st_name):
        
        lines = self._st_lines
        class_grades = {}
        for line in lines:
            line_split = line.split('_')
            temp_student = line_split[1].split(':')
            temp_grade = temp_student[1].split('\t')
            if line_split[0] == str(st_class):
                class_grades[temp_student[0]] = sum([int(g) for g in temp_grade])
        return [ self.get_ranking(st_name, class_grades), len(class_grades) ]
                 
                     
    def view_student_grade(self, student_cls, name):
        """ View student grade
        Args : name(student name) 
        Returns : 0(null)
        """
        avg = {}
        math = {}
        english = {}
        korean = {}
        physics = {}
        alchemy = {}
        
        lines = self._st_lines
        total = len(lines)
        
        # select DB
        for line in lines:
            student = line.split(':')[0]
            st_class = student.split('_')[0]
            st_name = student.split('_')[1]
            all_grade = line.split(':')[1].split('\t')
            sum = 0
            for x in all_grade:
                sum = sum + int(x)
            avg[st_name] = sum / len(all_grade)
            math[st_name] = int(all_grade[0])
            english[st_name] = int(all_grade[1])
            korean[st_name] = int(all_grade[2])
            physics[st_name] = int(all_grade[3])
            alchemy[st_name] = int(all_grade[4])
        cls_ranking , cls_total = self.student_clsranking(student_cls, name)
        # calculating grade
        grade_report = {}
        grade_report['personal'] = [student_cls, name]
        grade_report['cls_ranking'] = [total,
                                        cls_ranking,
                                        cls_total,
                                        round(cls_ranking / cls_total * 100, 2)
                                        ]
        grade_report['avg'] = [avg[name], 
                             StudentManager.get_ranking(name, avg),
                             total,
                             round(StudentManager.get_ranking(name, avg) / total * 100, 2)]
        grade_report['math'] = [math[name], 
                             StudentManager.get_ranking(name, math),
                             total,
                             round(StudentManager.get_ranking(name, math) / total * 100, 2)]
        grade_report['english'] = [english[name], 
                             StudentManager.get_ranking(name, english),
                             total,
                             round(StudentManager.get_ranking(name, english) / total * 100, 2)]
        grade_report['korean'] = [korean[name], 
                             StudentManager.get_ranking(name, korean),
                             total,
                             round(StudentManager.get_ranking(name, korean) / total * 100, 2)]
        grade_report['physics'] = [physics[name], 
                             StudentManager.get_ranking(name, physics),
                             total,
                             round(StudentManager.get_ranking(name, physics) / total * 100, 2)]
        grade_report['alchemy'] = [alchemy[name], 
                             StudentManager.get_ranking(name, alchemy),
                             total,
                             round(StudentManager.get_ranking(name, alchemy) / total * 100, 2)]
        
        return grade_report


    def view_class_grade(self):
        
        lines = self._st_lines
        class_grades = {}
        class_total = {}
        for line in lines:
            line_split = line.split('_')
            temp_student = line_split[1].split(':')
            temp_grade = temp_student[1].split('\t')
            if line_split[0] not in class_grades.keys():
                class_grades[line_split[0]] = sum([int(g) for g in temp_grade])
                class_total[line_split[0]] = 1
            else:
                class_grades[line_split[0]] += sum([int(g) for g in temp_grade])
                class_total[line_split[0]] += 1
        
        class_avg = {}
        for cls_number in class_grades.keys():
            class_avg[cls_number] = round( class_grades[cls_number] / class_total[cls_number] , 2 )
        sorted_list = sorted(class_avg.items(), key=operator.itemgetter(1),reverse=True)
        sorted_dic = {}
        for i in sorted_list:
            sorted_dic[i[0]]=i[1]
        return sorted_dic

                
    
    def write_grade(self, classes, name, math, english, korean, physics, alchemy):
        fr = open("./grade.txt", 'r')
        lines = fr.readlines()
        
        count = 0
        
        for line in lines:
            if line.find(name) >= 0:
                count = count + 1
                
        if count > 0:
            name = name + str(count)
            print(name)
        
        f =  open("./grade.txt", 'a')
        student = '{}_{}:{}\t{}\t{}\t{}\t{}'.format(
                    classes,
                    name,
                    math,
                    english,
                    korean,
                    physics,
                    alchemy
                    )
        f.write(student)
        f.write('\n')
        f.close()
        return "Success"
#    @staticmethod
#    def write_rd_grade(loop):
#        
      

if __name__ == '__main__':
    
    sm = StudentManager()
    #sm.view_class_grade()
    #sm.write_grade(13, '구승재', 100, 50, 0, 10, 80)
    sm.view_student_grade(13,'구승재')
