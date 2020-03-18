from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import QTUser, Review, Class

class QTUserAdmin(admin.ModelAdmin):
    model = QTUser
    list_display = ['username', 'first_name','last_name']
    fields = ['email', 'username', 'first_name', 'last_name', 'year']

class ClassAdmin(admin.ModelAdmin):
    model = Class
    list_display = ['class_name', 'dept', 'course_num']
    fields = ['class_name', 'dept', 'course_num']


admin.site.register(QTUser, QTUserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Review)

