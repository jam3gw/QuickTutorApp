from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from enum import Enum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from postgres_copy import CopyManager


class QTUser(AbstractUser):
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=30)
    year = models.IntegerField(null=True)
    rough_payment_per_hour = models.IntegerField(blank=True, null=True)
    rough_willing_to_pay_per_hour = models.IntegerField(blank=True, null= True)
    
    def __str__(self):
        return self.username + " (" + self.first_name + " " + self.last_name + ")"


class Class(models.Model):
    class_name = models.CharField(max_length=50)
    dept = models.CharField(max_length = 6, default="XXXX")
    course_num = models.IntegerField(default="0000")
    course_topic = models.CharField(max_length=100, default="", null=True)
    full_id = models.CharField(max_length=200, default="", null=False, unique=True)
    objects = CopyManager()

    def __str__(self):
        return str(self.dept) + str(self.course_num) + " (" + str(self.class_name) + ")"

class Session(models.Model):
    PENDING = '0'
    REJECTED = '1'
    ACCEPTED = '2'
    SESSION_CHOICES = [(PENDING, 'pending'),(REJECTED,'rejected'), (ACCEPTED, 'accepted')]

    student = models.ForeignKey(QTUser, related_name="Student", on_delete=models.CASCADE)
    tutor = models.ForeignKey(QTUser, related_name="Tutor", on_delete=models.CASCADE) 
    subject_in_regards_to = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_date_and_time = models.DateTimeField(null = False, default=timezone.now())
    end_date_and_time = models.DateTimeField(null = False, default=(timezone.now() + timedelta(hours=1)))
    student_proposal = models.CharField(null = False, choices = SESSION_CHOICES, default=PENDING, max_length=1)
    tutor_proposal = models.CharField(null = False, choices = SESSION_CHOICES, default=PENDING, max_length=1)
    price_of_tutor = models.IntegerField(blank=True, null= True)

    def __str__(self):
        return str(self.student) + " is having a session with " + str(self.tutor) + " in " + str(self.subject_in_regards_to) + " " + str(self.start_date_and_time) + " until " + str(self.end_date_and_time)

class Review(models.Model):
    # For who is being reviewed
    STUDENT = 'S'
    TUTOR = 'T'
    STUDENT_OR_TUTOR_CHOICES = [(STUDENT, 'of the student'),(TUTOR,'of the tutor')]

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RATING_CHOICES = [(ONE, '1'), (TWO, '2'), (THREE,'3'),(FOUR,'4'), (FIVE,'5')]

    Author = models.ForeignKey(QTUser, related_name = "Author", on_delete=models.CASCADE)
    Recipient = models.ForeignKey(QTUser,related_name="Recipient", on_delete=models.CASCADE)
    subject_in_regards_to = models.ForeignKey(Class, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null=False,choices= RATING_CHOICES, default = THREE)
    description = models.TextField()
    type_of_review = models.CharField(max_length = 1, choices = STUDENT_OR_TUTOR_CHOICES, default = TUTOR)
    time_of_review = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.Author) + "'s review of " + str(self.Recipient)
    
class ClassNeedsHelp(models.Model):
    user = models.ForeignKey(QTUser, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class,  on_delete=models.CASCADE)
    elaboration = models.TextField(max_length = None, primary_key= False)

    def __str__(self):
        return str(self.user) + " needs help in " + str(self.class_id)
        
class TutorableClass(models.Model):
    user = models.ForeignKey(QTUser, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    TA = models.BooleanField(name="Former_TA", default=False)
    experience_detail = models.TextField(name="experience", max_length=None)

    def __str__(self):
        if(self.Former_TA):
           return str(self.user) + " can tutor in " + str(self.class_id) + " and they are a former TA."
        else:
            return str(self.user) + " can tutor in " + str(self.class_id)

