from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class QTUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

    
