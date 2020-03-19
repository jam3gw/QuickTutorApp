from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from enum import Enum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class QTUser(AbstractUser):
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=30)
    year = models.IntegerField(null=True)
    
    def __str__(self):
        return self.username


class Class(models.Model):
    class_name = models.CharField(max_length=50)
    dept = models.CharField(max_length = 6, default="XXXX")
    course_num = models.IntegerField(default="0000")

    def __str__(self):
        return str(self.dept) + str(self.course_num) + " (" + str(self.class_name) + ")"

class Session(models.Model):
    Student = models.ManyToManyField(QTUser, related_name="Student", default = 1)
    Tutor = models.ManyToManyField(QTUser, related_name="Tutor", default = 1) 
    subject_in_regards_to = models.ManyToManyField(Class, default = 1)
    date_and_time = models.DateTimeField(null = False)
    duration_of_session = models.DurationField(null = False)

    def __str__(self):
        return str(Student) + " is having a session with " + str(Tutor) + " in " + str(subject_in_regards_to) + " " + str(date_and_time) + " for " + str(length)


TUTOR_OR_STUDENT=[('S','Student'),('T','Tutor')]

class Review(models.Model):
    Author = models.ManyToManyField(QTUser, related_name = "Author", default = 1)
    Recipient = models.ManyToManyField(QTUser,related_name="Recipient", default = 1)
    subject_in_regards_to = models.ManyToManyField(Class, default = 1)
    rating = models.IntegerField(null=False,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],help_text="Please rate your experience.")
    description = models.TextField(help_text="Please enter some additional information regarding your experience")
    isTutor = models.BooleanField()
    time_of_review = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(Author) + "'s review of " + str(Recipient)

    
class ClassNeedsHelp(models.Model):
    user = models.ManyToManyField(QTUser, default = 1)
    class_id = models.ManyToManyField(Class,  default = 1)
    elaboration = models.TextField(max_length = None, primary_key= False)

    def __str__(self):
        return str(user) + " needs help in " + str(class_id)
        

class TutorableClass(models.Model):
    user = models.ManyToManyField(QTUser, default = 1)
    class_id = models.ManyToManyField(Class, default = 1)
    TA = models.BooleanField(name="TA", default=False)
    experience_detail = models.TextField(name="experience", max_length=None)

    def __str__(self):
        return str(user) + " can tutor in " + str(class_id)

