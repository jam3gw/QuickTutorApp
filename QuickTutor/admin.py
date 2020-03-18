from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import QTUser, Review, Class

class QTUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = QTUser
    list_display = ['email', 'username']

class ClassAdmin(admin.ModelAdmin):
    model = Class
    fields = ['class_name', 'dept', 'course_num']


admin.site.register(QTUser, QTUserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Review)

