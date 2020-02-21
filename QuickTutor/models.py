from django.conf import settings
from django.db import models

class QTUser(models.Model):
    email = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )

    
