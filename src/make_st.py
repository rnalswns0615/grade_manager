# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 16:04:13 2019

@author: 구상수
"""
import numpy
from sm_helper import StudentManager
#from random import *
import random


if __name__ == '__main__':
    sm = StudentManager()
    
    firstname = ['김','이','박','최','정','강','조','윤','장','임']
    middlename = ['민','준','상','영','정','현','동','지','승','도']
    lastname = ['수','호','우','혁','석','준','훈','현','민','재']
    
    for x in range(0,300):
        name = '{}{}{}'.format(numpy.random.choice(firstname),
                               numpy.random.choice(middlename),
                               numpy.random.choice(lastname))
        
    
        sm.write_grade(name, 
                       random.randint(0,100),
                       random.randint(0,100), 
                       random.randint(0,100), 
                       random.randint(0,100), 
                       random.randint(0,100))
