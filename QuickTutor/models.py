from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from enum import Enum

class QTUser(AbstractUser):
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=30)
    #year = models.IntegerField(max_length=1)

class Student(QTUser):
    student_user = models.OneToOneField(QTUser, on_delete= models.CASCADE, parent_link=True, default=1)
    def addClass(self, class_name, classID):
        newClass = Class(QTUser = super.self, name= class_name, classID = classID, tutorable = False, TA_experience = False)
        self.classes_need_help.append(newClass)
        
    def removeClass(self, classID):
        for c in self.classes_need_help:
            if c.classID == classID:
                self.classes_need_help.remove(c)
                break

class Tutor(QTUser):
    tutor_user = models.OneToOneField(QTUser, on_delete= models.CASCADE, parent_link=True, default=1)
    classes_can_help = []

    def addClass(self, class_name, classID, TA_experience):
        newClass = Class(QTUser = super.self, name= class_name, classID = classID, tutorable = True, TA_experience = TA_experience)
        self.classes_need_help.append(newClass)
        
    def removeClass(self, classID):
        for c in self.classes_need_help:
            if c.classID == classID:
                self.classes_need_help.remove(c)
                break


class Class(models.Model):
    QTUser = models.ManyToManyField(QTUser)
    class_name = models.CharField(max_length=30, null=False)
    classID = models.CharField(max_length = 6, default="XX0000", primary_key=True, null=False)
    tutorable = models.BooleanField()
    TA_experience = models.BooleanField()

class Review(models.Model):
    Author = models.ManyToManyField(QTUser, related_name="Author")
    Recipient = models.ManyToManyField(QTUser,related_name="Recipient")
    subject_in_regards_to = models.CharField(max_length=30, null=False)
    rating = models.IntegerField(null=False,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],help_text="Please rate your experience.")
    description = models.TextField(help_text="Please enter some additional information regarding your experience")

    
