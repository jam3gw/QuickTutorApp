from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import QTUser, Review, Class, ClassNeedsHelp, TutorableClass

class classNeedsHelpInLine(admin.TabularInline):
    model = ClassNeedsHelp
    extra = 1

class QTUserAdmin(admin.ModelAdmin):
    model = QTUser
    list_display = ['username', 'first_name','last_name']
    fields = ['email', 'username', 'first_name', 'last_name', 'year']
    inlines = (classNeedsHelpInLine,)

class ClassAdmin(admin.ModelAdmin):
    model = Class
    list_display = ['class_name', 'dept', 'course_num']
    fields = ['class_name', 'dept', 'course_num']
    inlines = (classNeedsHelpInLine,)

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    # list_display = ('author', 'recipient')
    # fields = ['author', 'recipient', 'subject_in_regards_to', 'rating', 'description']

    # def getAuthor(self, obj):
    #     return "\n".join([p.products for p in obj.product.all()])

class ClassNeedsHelpAdmin(admin.ModelAdmin):
    model = ClassNeedsHelp
    list_diplay = ['user', 'class_id']
    fields = ['user', 'class_id', 'elaboration']


class TutorableClassAdmin(admin.ModelAdmin):
    model = TutorableClass
    list_diplay = ['user', 'class_id']

admin.site.register(QTUser, QTUserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ClassNeedsHelp, ClassNeedsHelpAdmin)
admin.site.register(TutorableClass, TutorableClassAdmin)

