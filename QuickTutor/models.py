from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from enum import Enum

class QTUser(AbstractUser):
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=30)

    #year = models.IntegerField(max_length=1)

class Student(models.Model):
    student_user = models.OneToOneField(QTUser, on_delete= models.CASCADE, parent_link=True)

    # def addClass(self, class_name, classID):
    #     newClass = Class(QTUser = super.self, name= class_name, classID = classID, tutorable = False, TA_experience = False)
    #     self.classes_need_help.append(newClass)
        
    # def removeClass(self, classID):
    #     for c in self.classes_need_help:
    #         if c.classID == classID:
    #             self.classes_need_help.remove(c)
    #             break

class Tutor(models.Model):
    tutor_user = models.OneToOneField(QTUser, on_delete= models.CASCADE, parent_link=True)

    # def addClass(self, class_name, classID, TA_experience):
    #     newClass = Class(QTUser = super.self, name= class_name, classID = classID, tutorable = True, TA_experience = TA_experience)
    #     self.classes_need_help.append(newClass)
        
    # def removeClass(self, classID):
    #     for c in self.classes_need_help:
    #         if c.classID == classID:
    #             self.classes_need_help.remove(c)
    #             break

class Class(models.Model):
    class_name = models.CharField(max_length=30, null=False)
    classID = models.CharField(max_length = 6, default="XX0000", primary_key=True, null=False)

    def __init__(self, class_name, classID):
        self.class_name = class_name
        self.class_id = class_id 

    def __str__(self):
        return self.class_name

class Review(models.Model):
    Author = models.ManyToManyField(QTUser, related_name="Author")
    Recipient = models.ManyToManyField(QTUser,related_name="Recipient")
    subject_in_regards_to = models.CharField(max_length=30, null=False)
    rating = models.IntegerField(null=False,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],help_text="Please rate your experience.")
    description = models.TextField(help_text="Please enter some additional information regarding your experience")

    
class ClassNeedsHelp(models.Model):
    student = models.ManyToManyField(Student)
    class_id = models.ManyToManyField(Class)
    elaboration = models.TextField(max_length = None, primary_key= False)

    def __init__(self, Student, Class, elaboration):
        self.student = Student
        self.class_id = Class
        self.elaboration = elaboration
        self.save()
        

class TutorableClass(models.Model):
    tutor = models.ManyToManyField(Tutor)
    class_id = models.ManyToManyField(Class)
    TA_example = models.BooleanField(name="TA", default=False)
    experience_detail = models.TextField(name="experience", max_length=None)

