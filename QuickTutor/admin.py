from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import QTUser, Review, Class, ClassNeedsHelp, TutorableClass, Session

class QTUserAdmin(admin.ModelAdmin):
    model = QTUser
    list_display = ['username', 'first_name','last_name']
    fields = ['email', 'username', 'first_name', 'last_name', 'year']

class ClassAdmin(admin.ModelAdmin):
    model = Class
    list_display = ['class_name', 'dept', 'course_num']
    fields = ['class_name', 'dept', 'course_num']

class SessionAdmin(admin.ModelAdmin):
    model = Session
    # list_display = ['Student', 'Tutor']
    fields = ['date_and_time', 'length']
    filter_horizontal = ['Student', 'Tutor', 'subject_in_regards_to']


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    # list_display = ['Author', 'Recipient']
    fields = [ 'rating', 'description', 'isTutor', 'time_of_review']
    filter_horizontal = ['Author', 'Recipient', 'subject_in_regards_to']

    # def getAuthor(self, obj):
    #     return "\n".join([p.products for p in obj.product.all()])


class ClassNeedsHelpAdmin(admin.ModelAdmin):
    model = ClassNeedsHelp
    # list_diplay = ['user', 'class_id']
    fields = ['elaboration']
    filter_horizontal = ['user', 'class_id']

class TutorableClassAdmin(admin.ModelAdmin):
    model = TutorableClass
    # list_diplay = ['user', 'class_id']
    fields = ['TA','experience_detail']
    filter_horizontal = ['user', 'class_id']


admin.site.register(QTUser, QTUserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(ClassNeedsHelp, ClassNeedsHelpAdmin)
admin.site.register(TutorableClass, TutorableClassAdmin)

