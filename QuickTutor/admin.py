from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import QTUser, Student , Tutor, Review, Class

class QTUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = QTUser
    list_display = ['email', 'username']

class StudentAdmin(UserAdmin):
    model = Student
    list_display = ['email','username','i_am_student']


admin.site.register(QTUser, QTUserAdmin)
admin.site.register(Class)
admin.site.register(Review)

