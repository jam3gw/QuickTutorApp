from django.db import models
from django.contrib.auth.models import AbstractUser

class QTUser(AbstractUser):
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=30)
    #year = models.IntegerField(max_length=1)
    pass

    class Student(models.Model):
        QTUser = models.ForeignKey(QTUser, on_delete=models.CASCADE)
        classes_need_help = []

        def addClass(self, class_name, classID):
            newClass = Class(QTUser = self, name= class_name, classID = classID, tutorable = False, TA_experience = False)
            self.classes_need_help.append(newClass)
        
        def removeClass(self, classID):
            for c in self.classes_need_help:
                if c.classID == classID:
                    self.classes_need_help.remove(c)
                    break

    class Tutor(models.Model):
        QTUser = models.ForeignKey(QTUser, on_delete=models.CASCADE)
        classes_can_help = []

        def addClass(self, class_name, classID, TA_experience):
            newClass = Class(QTUser = self, name= class_name, classID = classID, tutorable = True, TA_experience = TA_experience)
            self.classes_need_help.append(newClass)
        
        def removeClass(self, classID):
            for c in self.classes_need_help:
                if c.classID == classID:
                    self.classes_need_help.remove(c)
                    break


class Class(models.Model):
    QTUser = models.ManyToManyField(QTUser)
    name = models.CharField(max_length=30, null=False)
    classID = models.CharField(max_length = 6, default="XX0000", primary_key=True, null=False)
    tutorable = models.BooleanField()
    TA_experience = models.BooleanField()


    
