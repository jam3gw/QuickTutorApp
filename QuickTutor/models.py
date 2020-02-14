from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(User):
    email = User.email
    username = User.email
    password = User.password
    first_name = User.first_name
    last_name = User.last_name

    def __str__(self):
        return self.username
