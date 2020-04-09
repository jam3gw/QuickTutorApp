from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordResetView
from django.views import generic
from django.http import JsonResponse
from django.conf import settings
from . import forms
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
    SyncGrant,
    ChatGrant
)
from .models import QTUser, Review, Session, Class, ClassNeedsHelp, TutorableClass
from .forms import ClassNeedsHelpForm, TutorableClassForm, SessionForm, ReviewForm, EditProfileForm
from django.core.mail import send_mail

def index(request):
    return render(request, 'QuickTutor/index.html', {})
# Create your views here.

def app(request):
    return render(request, 'twilio/index.html')

def token(request):
    current_user = request.user
    return generateToken(current_user.first_name + " " + current_user.last_name)

def generateToken(identity):
    # Get credentials from environment variables
    account_sid      = settings.TWILIO_ACCT_SID
    chat_service_sid = settings.TWILIO_CHAT_SID
    sync_service_sid = settings.TWILIO_SYNC_SID
    api_sid          = settings.TWILIO_API_SID
    api_secret       = settings.TWILIO_API_SECRET

    # Create access token with credentials
    token = AccessToken(account_sid, api_sid, api_secret, identity=identity)

    # Create a Sync grant and add to token
    if sync_service_sid:
        sync_grant = SyncGrant(service_sid=sync_service_sid)
        token.add_grant(sync_grant)

    # Create a Chat grant and add to token
    if chat_service_sid:
        chat_grant = ChatGrant(service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    # Return token info as JSON
    return JsonResponse({'identity':identity,'token':token.to_jwt().decode('utf-8')})

class ProfileView(generic.TemplateView):
    template_name = 'QuickTutor/profile.html'

    def get(self,request):
        user = request.user

        #sessions participated in 
        student_sessions = list(Session.objects.filter(student = user).order_by('-start_date_and_time'))
        tutor_sessions = list(Session.objects.filter(tutor = user).order_by('-start_date_and_time'))

        #classes need help in/can tutor in 
        classes_need_help_in = list(ClassNeedsHelp.objects.filter(user = user))
        classes_can_tutor_in = list(TutorableClass.objects.filter(user = user))

        #reviews
        reviews_received = list(Review.objects.filter(Recipient = user).order_by('-time_of_review'))

        reviews_written = list(Review.objects.filter(Author = user).order_by('-time_of_review'))

        average_rating = list(Review.objects.filter(Recipient = user).values('rating')) #returns dictionary
        if (len(average_rating) != 0):
            current_rating_sum = 0
            current_num_ratings = 0
            for rating in average_rating:
                current_rating_sum += rating['rating']
                current_num_ratings += 1
                
            average_rating = current_rating_sum/ current_num_ratings
        else:
            average_rating = 0
            current_num_ratings = 0


        context_objects = {
            'user' : user,
            'student_sessions': student_sessions,
            'tutor_sessions' : tutor_sessions,
            'classes_need_help_in' : classes_need_help_in,
            'classes_can_tutor_in' : classes_can_tutor_in,
            'reviews_received' : reviews_received,
            'reviews_written' : reviews_written,
            'average_rating' : average_rating,
            'ratings_received' : current_num_ratings
        }
        return render(request, self.template_name, context = context_objects)

class SessionsView(generic.TemplateView):
    template_name = "QuickTutor/ViewSessions.html"

    def get(self,request):
        user = request.user
        student_sessions = list(Session.objects.filter(student = user).order_by('-start_date_and_time'))
        tutor_sessions = list(Session.objects.filter(tutor = user).order_by('-start_date_and_time'))

        context_objects = {
            'student_sessions' : student_sessions,
            'tutor_sessions' : tutor_sessions,
        }
        return render(request, self.template_name, context = context_objects)

class ReviewsView(generic.TemplateView):
    template_name = "QuickTutor/ReadReviews.html"

    def get(self,request):
        user = request.user
        reviews_received = list(Review.objects.filter(Recipient = user).order_by('-time_of_review'))
        reviews_written = list(Review.objects.filter(Author = user).order_by('-time_of_review'))

        context_objects = {
            'reviews_received' : reviews_received,
            'reviews_written' : reviews_written,
        }
        return render(request, self.template_name, context = context_objects)

#forms stuff
def Add_Class_Needs_Help(request):

    form = ClassNeedsHelpForm(request.POST)

    if form.is_valid():
        new_class_needs_help = form.save(commit=False)
        new_class_needs_help.user = request.user
        new_class_needs_help.save()
        print('valid')

        return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClassNeedsHelpForm()
        print("incorrect", form.data)
        
    return render(request, 'QuickTutor/ClassNeedsHelpForm.html', {'form': form})

def Add_Tutorable_Class(request):

    form = TutorableClassForm(request.POST)

    if form.is_valid():
        new_class_can_tutor = form.save(commit=False)
        new_class_can_tutor.user = request.user
        new_class_can_tutor.save()
        print('valid')

        return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TutorableClassForm()
        print("incorrect", form.data)
        
    return render(request, 'QuickTutor/TutorableClassForm.html', {'form': form})

def Add_Review_Class(request):
    # if this is a POST request we need to process the form data
    form = ReviewForm(request.POST)

    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.Author = request.user
        new_review.save()
        print('valid')

        return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReviewForm()
        print("incorrect", form.data)
        
    return render(request, 'QuickTutor/ReviewForm.html', {'form': form})

def edit_Profile_Class(request):
    # if this is a POST request we need to process the form data
    form = EditProfileForm(request.POST)
    userObject = QTUser.objects.get(username = request.user.username)
    if form.is_valid():
        userObject.first_name = form.cleaned_data['first_name']
        userObject.last_name = form.cleaned_data['last_name']
        userObject.year = form.cleaned_data['year']
        userObject.rough_payment_per_hour = form.cleaned_data['rough_payment_per_hour']
        userObject.rough_willing_to_pay_per_hour = form.cleaned_data['rough_willing_to_pay_per_hour']
        userObject.save()
        print('valid')

        return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditProfileForm()
        print("incorrect", form.data)
        
    return render(request, 'QuickTutor/editProfile.html', {'form': form})

def SendEmail(request):
    sub = forms.SetupSession()
    if request.method == 'POST':
        sub = forms.SetupSession(request.POST)
        subject = "Tutor Request [DO NOT REPLY]"
        message = 'Hi my name is ' + str(request.user.first_name) + " and I can tutor you for " + str(request.user.rough_payment_per_hour)
        recepient = str(sub['Email'].value())
        send_mail(subject, message, request.user.email ,[recepient], fail_silently = False)
        return render(request, 'QuickTutor/success.html', {'recepient': recepient})
    return render(request, 'Quicktutor/Sessions.html', {'form':sub})

# def Create_Session_Class(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = ReviewForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/profile/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = ReviewForm()
        
#     return render(request, 'QuickTutor/ClassNeedsHelpForm.html', {'form': form})