from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#source: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class User(User):
    email = User.email
    password = User.password

    def __str__(self):
        return self.email

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    
