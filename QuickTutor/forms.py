from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import QTUser, Review, Class, ClassNeedsHelp, Session, TutorableClass
from django.forms import widgets

class ClassNeedsHelpForm(forms.ModelForm):
    class Meta:
        model = ClassNeedsHelp
        fields = ['class_id','elaboration']

class TutorableClassForm(forms.ModelForm):
    class Meta:
        model = TutorableClass
        fields = ['class_id','Former_TA', 'experience']

class CreateSessionForm(forms.ModelForm):
    # TIME_CHOICES = []
    # for k in ["AM","PM"]:
    #     for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
    #         for j in ['00','15','30','45']:
    #             time = (str(i)+":"+str(j) + " " + k,str(i)+":"+str(j) + " " + k)
    #             TIME_CHOICES.append(time)    
    # # TIME_TUPLE = tuple(TIME_CHOICES)
    # print(TIME_TUPLE)

    time_slots = (('12:00 AM', '12:00 AM'), ('12:15 AM', '12:15 AM'), ('12:30 AM', '12:30 AM'), ('12:45 AM', '12:45 AM'),
    ('1:00 AM', '1:00 AM'), ('1:15 AM', '1:15 AM'), ('1:30 AM', '1:30 AM'), ('1:45 AM', '1:45 AM'), 
    ('2:00 AM', '2:00 AM'), ('2:15 AM', '2:15 AM'), ('2:30 AM', '2:30 AM'), ('2:45 AM', '2:45 AM'), ('3:00 AM', '3:00 AM'), 
    ('3:15 AM', '3:15 AM'), ('3:30 AM', '3:30 AM'), ('3:45 AM', '3:45 AM'), ('4:00 AM', '4:00 AM'), ('4:15 AM', '4:15 AM'), 
    ('4:30 AM', '4:30 AM'), ('4:45 AM', '4:45 AM'), ('5:00 AM', '5:00 AM'), ('5:15 AM', '5:15 AM'), ('5:30 AM', '5:30 AM'), 
    ('5:45 AM', '5:45 AM'), ('6:00 AM', '6:00 AM'), ('6:15 AM', '6:15 AM'), ('6:30 AM', '6:30 AM'), ('6:45 AM', '6:45 AM'), 
    ('7:00 AM', '7:00 AM'), ('7:15 AM', '7:15 AM'), ('7:30 AM', '7:30 AM'), ('7:45 AM', '7:45 AM'), ('8:00 AM', '8:00 AM'), 
    ('8:15 AM', '8:15 AM'), ('8:30 AM', '8:30 AM'), ('8:45 AM', '8:45 AM'), ('9:00 AM', '9:00 AM'), ('9:15 AM', '9:15 AM'), 
    ('9:30 AM', '9:30 AM'), ('9:45 AM', '9:45 AM'), ('10:00 AM', '10:00 AM'), ('10:15 AM', '10:15 AM'), ('10:30 AM', '10:30 AM'), 
    ('10:45 AM', '10:45 AM'), ('11:00 AM', '11:00 AM'), ('11:15 AM', '11:15 AM'), ('11:30 AM', '11:30 AM'), ('11:45 AM', '11:45 AM'), 
    ('12:00 PM', '12:00 PM'), ('12:15 PM', '12:15 PM'), ('12:30 PM', '12:30 PM'), ('12:45 PM', '12:45 PM'), ('1:00 PM', '1:00 PM'), 
    ('1:15 PM', '1:15 PM'), ('1:30 PM', '1:30 PM'), ('1:45 PM', '1:45 PM'), ('2:00 PM', '2:00 PM'), ('2:15 PM', '2:15 PM'), 
    ('2:30 PM', '2:30 PM'), ('2:45 PM', '2:45 PM'), ('3:00 PM', '3:00 PM'), ('3:15 PM', '3:15 PM'), ('3:30 PM', '3:30 PM'), 
    ('3:45 PM', '3:45 PM'), ('4:00 PM', '4:00 PM'), ('4:15 PM', '4:15 PM'), ('4:30 PM', '4:30 PM'), ('4:45 PM', '4:45 PM'), 
    ('5:00 PM', '5:00 PM'), ('5:15 PM', '5:15 PM'), ('5:30 PM', '5:30 PM'), ('5:45 PM', '5:45 PM'), ('6:00 PM', '6:00 PM'), 
    ('6:15 PM', '6:15 PM'), ('6:30 PM', '6:30 PM'), ('6:45 PM', '6:45 PM'), ('7:00 PM', '7:00 PM'), ('7:15 PM', '7:15 PM'), 
    ('7:30 PM', '7:30 PM'), ('7:45 PM', '7:45 PM'), ('8:00 PM', '8:00 PM'), ('8:15 PM', '8:15 PM'), ('8:30 PM', '8:30 PM'), 
    ('8:45 PM', '8:45 PM'), ('9:00 PM', '9:00 PM'), ('9:15 PM', '9:15 PM'), ('9:30 PM', '9:30 PM'), ('9:45 PM', '9:45 PM'), 
    ('10:00 PM', '10:00 PM'), ('10:15 PM', '10:15 PM'), ('10:30 PM', '10:30 PM'), ('10:45 PM', '10:45 PM'), ('11:00 PM', '11:00 PM'),
     ('11:15 PM', '11:15 PM'), ('11:30 PM', '11:30 PM'), ('11:45 PM', '11:45 PM'))

    YEAR_CHOICES = ['2020']
    date = forms.DateTimeField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))
    start_time = forms.ChoiceField(choices=time_slots)
    end_time = forms.ChoiceField(choices=time_slots)
    # start_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'],initial="M/D/Y Hour:Minute am/pm")
    # end_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'],initial="M/D/Y Hour:Minute am/pm")

    class Meta:
        model = Session
        fields = ['tutor','subject_in_regards_to','price_of_tutor']
    
    def __init__(self, user, *args, **kwargs):
        super(CreateSessionForm, self).__init__(*args, **kwargs)
        class_possibilities_list = []
        tutor_possibilities_list = []

        for c in ClassNeedsHelp.objects.filter(user=user).values_list('class_id'):
            class_possibilities_list.append(c[0])

        for c in TutorableClass.objects.filter(user=user).values_list('class_id'):
            class_possibilities_list.append(c[0])
        
        for t in Session.objects.filter(student=user).filter(tutor_proposal='2').values_list('tutor'):
            tutor_possibilities_list.append(t[0])
        
        self.fields['subject_in_regards_to'].queryset = Class.objects.filter(id__in=class_possibilities_list)
        self.fields['tutor'].queryset = QTUser.objects.filter(pk__in = tutor_possibilities_list)


class CreateSpecificSessionForm(forms.ModelForm):
    time_slots = (('12:00 AM', '12:00 AM'), ('12:15 AM', '12:15 AM'), ('12:30 AM', '12:30 AM'), ('12:45 AM', '12:45 AM'),
    ('1:00 AM', '1:00 AM'), ('1:15 AM', '1:15 AM'), ('1:30 AM', '1:30 AM'), ('1:45 AM', '1:45 AM'), 
    ('2:00 AM', '2:00 AM'), ('2:15 AM', '2:15 AM'), ('2:30 AM', '2:30 AM'), ('2:45 AM', '2:45 AM'), ('3:00 AM', '3:00 AM'), 
    ('3:15 AM', '3:15 AM'), ('3:30 AM', '3:30 AM'), ('3:45 AM', '3:45 AM'), ('4:00 AM', '4:00 AM'), ('4:15 AM', '4:15 AM'), 
    ('4:30 AM', '4:30 AM'), ('4:45 AM', '4:45 AM'), ('5:00 AM', '5:00 AM'), ('5:15 AM', '5:15 AM'), ('5:30 AM', '5:30 AM'), 
    ('5:45 AM', '5:45 AM'), ('6:00 AM', '6:00 AM'), ('6:15 AM', '6:15 AM'), ('6:30 AM', '6:30 AM'), ('6:45 AM', '6:45 AM'), 
    ('7:00 AM', '7:00 AM'), ('7:15 AM', '7:15 AM'), ('7:30 AM', '7:30 AM'), ('7:45 AM', '7:45 AM'), ('8:00 AM', '8:00 AM'), 
    ('8:15 AM', '8:15 AM'), ('8:30 AM', '8:30 AM'), ('8:45 AM', '8:45 AM'), ('9:00 AM', '9:00 AM'), ('9:15 AM', '9:15 AM'), 
    ('9:30 AM', '9:30 AM'), ('9:45 AM', '9:45 AM'), ('10:00 AM', '10:00 AM'), ('10:15 AM', '10:15 AM'), ('10:30 AM', '10:30 AM'), 
    ('10:45 AM', '10:45 AM'), ('11:00 AM', '11:00 AM'), ('11:15 AM', '11:15 AM'), ('11:30 AM', '11:30 AM'), ('11:45 AM', '11:45 AM'), 
    ('12:00 PM', '12:00 PM'), ('12:15 PM', '12:15 PM'), ('12:30 PM', '12:30 PM'), ('12:45 PM', '12:45 PM'), ('1:00 PM', '1:00 PM'), 
    ('1:15 PM', '1:15 PM'), ('1:30 PM', '1:30 PM'), ('1:45 PM', '1:45 PM'), ('2:00 PM', '2:00 PM'), ('2:15 PM', '2:15 PM'), 
    ('2:30 PM', '2:30 PM'), ('2:45 PM', '2:45 PM'), ('3:00 PM', '3:00 PM'), ('3:15 PM', '3:15 PM'), ('3:30 PM', '3:30 PM'), 
    ('3:45 PM', '3:45 PM'), ('4:00 PM', '4:00 PM'), ('4:15 PM', '4:15 PM'), ('4:30 PM', '4:30 PM'), ('4:45 PM', '4:45 PM'), 
    ('5:00 PM', '5:00 PM'), ('5:15 PM', '5:15 PM'), ('5:30 PM', '5:30 PM'), ('5:45 PM', '5:45 PM'), ('6:00 PM', '6:00 PM'), 
    ('6:15 PM', '6:15 PM'), ('6:30 PM', '6:30 PM'), ('6:45 PM', '6:45 PM'), ('7:00 PM', '7:00 PM'), ('7:15 PM', '7:15 PM'), 
    ('7:30 PM', '7:30 PM'), ('7:45 PM', '7:45 PM'), ('8:00 PM', '8:00 PM'), ('8:15 PM', '8:15 PM'), ('8:30 PM', '8:30 PM'), 
    ('8:45 PM', '8:45 PM'), ('9:00 PM', '9:00 PM'), ('9:15 PM', '9:15 PM'), ('9:30 PM', '9:30 PM'), ('9:45 PM', '9:45 PM'), 
    ('10:00 PM', '10:00 PM'), ('10:15 PM', '10:15 PM'), ('10:30 PM', '10:30 PM'), ('10:45 PM', '10:45 PM'), ('11:00 PM', '11:00 PM'),
     ('11:15 PM', '11:15 PM'), ('11:30 PM', '11:30 PM'), ('11:45 PM', '11:45 PM'))

    YEAR_CHOICES = ['2020']
    date = forms.DateTimeField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))
    start_time = forms.ChoiceField(choices=time_slots)
    end_time = forms.ChoiceField(choices=time_slots)
    class Meta:
        model = Session
        fields = ['subject_in_regards_to','price_of_tutor']

    def __init__(self, tutor_id, *args, **kwargs):
        super(CreateSpecificSessionForm, self).__init__(*args, **kwargs)
        possibilities_list = []

        for c in TutorableClass.objects.filter(user=tutor_id).values_list('class_id'):
            possibilities_list.append(c[0])
        
        print(possibilities_list)
        self.fields['subject_in_regards_to'].queryset = Class.objects.filter(id__in=possibilities_list)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['Recipient','subject_in_regards_to','rating','description','type_of_review']
    
    def __init__(self, user, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        class_possibilities_list = []
        review_possibilities_list = []

        for c in ClassNeedsHelp.objects.filter(user=user).values_list('class_id'):
            class_possibilities_list.append(c[0])

        for c in TutorableClass.objects.filter(user=user).values_list('class_id'):
            class_possibilities_list.append(c[0])
        
        self.fields['subject_in_regards_to'].queryset = Class.objects.filter(id__in=class_possibilities_list)

        for t in Session.objects.filter(student = user).filter(tutor_proposal='2').values_list('tutor'):
            review_possibilities_list.append(t[0])

        for s in Session.objects.filter(tutor = user).filter(student_proposal='2').values_list('student'):
            review_possibilities_list.append(s[0])
        
        self.fields['Recipient'].queryset = QTUser.objects.filter(pk__in=review_possibilities_list)


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

    