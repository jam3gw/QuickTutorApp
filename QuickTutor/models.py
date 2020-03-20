from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from enum import Enum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


class QTUser(AbstractUser):
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=30)
    year = models.IntegerField(null=True)
    rough_payment_per_hour =
    rough_willing_to_pay_per_hour = 
    
    def __str__(self):
        return self.username


class Class(models.Model):
    class_name = models.CharField(max_length=50)
    dept = models.CharField(max_length = 6, default="XXXX")
    course_num = models.IntegerField(default="0000")

    def __str__(self):
        return str(self.dept) + str(self.course_num) + " (" + str(self.class_name) + ")"

class Session(models.Model):
    student = models.ManyToManyField(QTUser, related_name="Student", default = '1')
    tutor = models.ManyToManyField(QTUser, related_name="Tutor", default = '1') 
    subject_in_regards_to = models.ManyToManyField(Class, default = '1')
    start_date_and_time = models.DateTimeField(null = False, default=timezone.now)
    end_date_and_time = models.DateTimeField(null = False, default=(timezone.now() + timedelta(hours=1))) 

    def __str__(self):
        # return str(self.student) + " is having a session with " + str(self.tutor) + " in " + str(self.subject_in_regards_to) + " " + str(self.start_date_and_time) + " until " + str(self.end_date_and_time)
        return "Session #:" + str(id)

class Review(models.Model):
    # For who is being reviewed
    STUDENT = 'S'
    TUTOR = 'T'
    STUDENT_OR_TUTOR_CHOICES = [(STUDENT, 'student'),(TUTOR,'tutor')]

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RATING_CHOICES = [(ONE, '1'), (TWO, '2'), (THREE,'3'),(FOUR,'4'), (FIVE,'5')]

    Author = models.ManyToManyField(QTUser, related_name = "Author", default = '1')
    Recipient = models.ManyToManyField(QTUser,related_name="Recipient", default = '1')
    subject_in_regards_to = models.ManyToManyField(Class, default = '1')
    rating = models.PositiveSmallIntegerField(null=False,choices= RATING_CHOICES, default = THREE ,help_text="Please rate your experience.")
    description = models.TextField(help_text="Please enter some additional information regarding your experience")
    type_of_review = models.CharField(max_length = 1, choices = STUDENT_OR_TUTOR_CHOICES, default = TUTOR)
    time_of_review = models.DateTimeField(default = timezone.now)

    def __str__(self):
        # return str(self.Author) + "'s review of " + str(self.Recipient)
        return "Review #:" + str(id)
    
class ClassNeedsHelp(models.Model):
    user = models.ManyToManyField(QTUser, default = '1')
    class_id = models.ManyToManyField(Class,  default = '1')
    elaboration = models.TextField(max_length = None, primary_key= False)

    def __str__(self):
        return str(self.user) + " needs help in " + str(self.class_id)
        

class TutorableClass(models.Model):
    user = models.ManyToManyField(QTUser, default = '1')
    class_id = models.ManyToManyField(Class, default = '1')
    TA = models.BooleanField(name="TA", default=False)
    experience_detail = models.TextField(name="experience", max_length=None)

    def __str__(self):
        return str(self.user) + " can tutor in " + str(self.class_id)

