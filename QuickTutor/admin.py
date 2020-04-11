from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import QTUser, Review, Class, ClassNeedsHelp, TutorableClass, Session

class QTUserAdmin(admin.ModelAdmin):
    model = QTUser
    list_display = ['username', 'first_name','last_name']
    fields = ['email', 'username', 'first_name', 'last_name', 'year', 'rough_payment_per_hour', 'rough_willing_to_pay_per_hour']

class ClassAdmin(admin.ModelAdmin):
    model = Class
    list_display = ['class_name', 'dept', 'course_num']
    fields = ['class_name', 'dept', 'course_num']

class SessionAdmin(admin.ModelAdmin):
    model = Session
    list_display = ['student', 'tutor', 'subject_in_regards_to']
    fields = ['student', 'tutor', 'subject_in_regards_to','start_date_and_time', 'end_date_and_time',
        'student_proposal', 'tutor_proposal', 'price_of_tutor']


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ['Author', 'Recipient', 'rating']
    fields = ['Author','Recipient', 'subject_in_regards_to','rating', 'description', 'type_of_review']


class ClassNeedsHelpAdmin(admin.ModelAdmin):
    model = ClassNeedsHelp
    # list_diplay = ['user', 'class_id']
    fields = ['user', 'class_id','elaboration']

class TutorableClassAdmin(admin.ModelAdmin):
    model = TutorableClass
    # list_diplay = ['user', 'class_id']
    fields = ['user', 'class_id','Former_TA','experience']


admin.site.register(QTUser, QTUserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(ClassNeedsHelp, ClassNeedsHelpAdmin)
admin.site.register(TutorableClass, TutorableClassAdmin)

