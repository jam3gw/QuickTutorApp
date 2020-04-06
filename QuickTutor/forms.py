from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import QTUser, Review, Class, ClassNeedsHelp, Session, TutorableClass

class ClassNeedsHelpForm(forms.ModelForm):
    class Meta:
        model = ClassNeedsHelp
        fields = ['class_id','elaboration']

class TutorableClassForm(forms.ModelForm):
    class Meta:
        model = TutorableClass
        fields = ['class_id','Former TA', 'experience']

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['Recipient','subject_in_regards_to','rating','description','type_of_review','time_of_review']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = QTUser
        fields = ['first_name','last_name','year','rough_payment_per_hour','rough_willing_to_pay_per_hour']



    