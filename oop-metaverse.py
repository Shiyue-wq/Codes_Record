# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:55:55 2022

@author: wangbenyou
"""
import random

class Examination:
    pass


class Registry:
    
    def __init__(self, students,instructors):
        self.students = students 
        self.instructors = instructors
        
    
    def main(self):
        for instructor in self.instructors:
            instructor.teach()
            
        for student in self.students:
            student.listen()
            

class Course:
    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name
        self.instructors = []
        self.teaching_instructor = None

    def regesiter_by_instrcutor(self, instructor):
        self.instructors.append(instructor)
        
        
class Student:
    def __init__(self, student_id, name, age, sex):
        self.student_id = student_id
        self.name = name
        self.age = name
        self.sex = sex
        self.selected_courses = []
    
    def select_course(self, course):
        instructor = random.choice(course.instructors)
        course.teaching_instructor = instructor
        print("{} selected a course {} taugh by Prof. {}".format(self.name,\
                  course.course_id, course.teaching_instructor.name ))
        self.selected_courses.append( course )
    
    def listen(self,):
        for course in self.selected_courses:
            print("{} listing couse {} taugh by {}".format(self.name,\
                  course.course_id, course.teaching_instructor.name ))

                  

class Instructor():
    def __init__(self, name):
        self.name = name
        self.courses = []
    
    def register_course(self, course):
        course.regesiter_by_instrcutor(self)
        self.courses.append(course)
        return
    
    def teach(self):
        if len(self.courses)== 0:
               print("{} does not need to teach".format(self.name))
               return            
        for course in self.courses:
            print("{} is teaching {}".format(self.name, course.name))


csc1001 = Course("CSC 1001", "python programing")
csc3100 = Course("CSC 3100", "data structure")

junhua = Instructor("junhua")
junhua.register_course(csc1001)

benyou = Instructor("benyou")
benyou.register_course(csc1001)
benyou.register_course(csc3100)

alice = Student("20000001", "alice", "20", "female")
bob = Student("20000001", "bob", "20", "male")

alice.select_course(csc1001)
bob.select_course(csc3100)
students = [bob, alice]
instructors = [benyou,junhua]

r = Registry(students,instructors)

r.main()













