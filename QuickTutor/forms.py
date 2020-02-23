from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import QTUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = QTUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = QTUser
        fields = ('username', 'email')
