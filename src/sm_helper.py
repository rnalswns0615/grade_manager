# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 20:51:34 2019

@author: 구상수
"""
import operator
from random import *


class StudentManager:
    def __init__(self):
        f =  open("C:/Users/구상수/.spyder-py3/study/grade.txt", 'r')
        lines = f.readlines()
        self._st_lines = lines
    
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
            if line_split[0] == st_class:
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
        print(grade_report)
        
        return 0


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
        sorted_dic = sorted(class_avg.items(), key=operator.itemgetter(1),reverse=True)
        print(sorted_dic)

                
    
    def write_grade(self, classes, name, math, english, korean, physics, alchemy):
        fr = open("C:/Users/구상수/.spyder-py3/study/grade.txt", 'r')
        lines = fr.readlines()
        
        count = 0
        
        for line in lines:
            if line.find(name) >= 0:
                count = count + 1
                
        if count > 0:
            name = name + str(count)
            print(name)
        
        f =  open("C:/Users/구상수/.spyder-py3/study/grade.txt", 'a')
        student = '{}_{}:{}\t{}\t{}\t{}\t{}'.format(
                    classes,
                    name,
                    math,
                    english,
                    korean,
                    physics,
                    alchemy
                    )
#        print(student)
        f.write('\n')
        f.write(student)
        f.close()
        
#    @staticmethod
#    def write_rd_grade(loop):
#        
      

if __name__ == '__main__':
    
    sm = StudentManager()
    sm.view_class_grade()

