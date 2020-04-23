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
        fields = ['class_id','Former_TA', 'experience']

class CreateSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['tutor', 'subject_in_regards_to', 'start_date_and_time',
        'end_date_and_time','price_of_tutor']

class CreateSpecificSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['subject_in_regards_to', 'start_date_and_time',
        'end_date_and_time','price_of_tutor']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['Recipient','subject_in_regards_to','rating','description','type_of_review','time_of_review']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = QTUser
        fields = ['first_name','last_name','year','rough_payment_per_hour','rough_willing_to_pay_per_hour']
    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()
        year = cleaned_data.get("year")
        print(year)
        rough_payment_per_hour = cleaned_data.get("rough_payment_per_hour")
        rough_willing_to_pay_per_hour = cleaned_data.get("rough_willing_to_pay_per_hour")
        if year:
            if year < 1 or year > 4:
                raise forms.ValidationError(
                    "Your year must be a value between 1-4"
                )
        if rough_payment_per_hour:
            if rough_payment_per_hour < 0 and rough_payment_per_hour > 256:
                raise forms.ValidationError(
                    "Your Hourly Rate must be a value between 1-256"
                )
        if rough_willing_to_pay_per_hour:
            if rough_willing_to_pay_per_hour < 0 and rough_willing_to_pay_per_hour > 256:
                raise forms.ValidationError(
                    "The amount you are willing to pay must be a value between 1-256"
                )
        return self.cleaned_data
# class SetupSession(forms.Form):
#     Email = forms.EmailField()
#     checkbox = forms.BooleanField()

#     def __str__(self):
#         return self.Email

    