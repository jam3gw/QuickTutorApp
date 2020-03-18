from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from enum import Enum
from django.db.models.signals import post_save
from django.dispatch import receiver


class QTUser(AbstractUser):
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=30)
    year = models.IntegerField(null=True)
    
    def __str__(self):
        return self.username


class Class(models.Model):
    class_name = models.CharField(max_length=50, null=False)
    dept = models.CharField(max_length = 6, default="XXXX", null=False)
    course_num = models.IntegerField(default="0000", null=False)

    def __str__(self):
        return str(self.dept) + str(self.course_num) + " (" + str(self.class_name) + ")"

class Review(models.Model):
    Author = models.ManyToManyField(QTUser, related_name="Author")
    Recipient = models.ManyToManyField(QTUser,related_name="Recipient")
    subject_in_regards_to = models.CharField(max_length=30, null=False)
    rating = models.IntegerField(null=False,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],help_text="Please rate your experience.")
    description = models.TextField(help_text="Please enter some additional information regarding your experience")

    
class ClassNeedsHelp(models.Model):
    user = models.ForeignKey(QTUser, on_delete=models.CASCADE, default = 1)
    class_id = models.ForeignKey(Class, on_delete= models.CASCADE, default = 1)
    elaboration = models.TextField(max_length = None, primary_key= False)
        

class TutorableClass(models.Model):
    user = models.ForeignKey(QTUser, on_delete=models.CASCADE, default = 1)
    class_id = models.ForeignKey(Class, on_delete= models.CASCADE, default = 1)
    TA_example = models.BooleanField(name="TA", default=False)
    experience_detail = models.TextField(name="experience", max_length=None)

