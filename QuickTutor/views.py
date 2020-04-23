from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordResetView
from django.views import generic
from django.http import JsonResponse
from django.conf import settings
from django.utils import dateparse
import datetime

from . import forms
import sys

from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
    SyncGrant,
    ChatGrant
)
from .models import QTUser, Review, Session, Class, ClassNeedsHelp, TutorableClass
from .forms import *
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone

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
    def post(self, request, **kwargs):
        return HttpResponseRedirect(request.path_info)
    def get(self,request):
        user = request.user
    
    
        #sessions participated in 

        accepted_student_sessions_future = Session.objects.filter(student = request.user, student_proposal = '2', tutor_proposal = '2',start_date_and_time__gte= datetime.datetime.now(timezone.get_current_timezone())).order_by('-start_date_and_time')
        accepted_tutor_sessions_future = Session.objects.filter(tutor = request.user, student_proposal = '2', tutor_proposal = '2',start_date_and_time__gte= datetime.datetime.now(timezone.get_current_timezone())).order_by('-start_date_and_time')

        accepted_student_sessions_past = Session.objects.filter(student = request.user, student_proposal = '2', tutor_proposal = '2', start_date_and_time__lt= datetime.datetime.now(timezone.get_current_timezone())).order_by('-start_date_and_time')
        accepted_tutor_sessions_past = Session.objects.filter(tutor = request.user, student_proposal = '2', tutor_proposal = '2',start_date_and_time__lt= datetime.datetime.now(timezone.get_current_timezone())).order_by('-start_date_and_time')
            
        pending_sessions_requested_student = Session.objects.filter(student = request.user, student_proposal = '2', tutor_proposal = '0').order_by('-start_date_and_time')
        pending_sessions_requested_tutor = Session.objects.filter(tutor = request.user, student_proposal = '0', tutor_proposal = '2').order_by('-start_date_and_time')
            
        waiting_acceptance_reject_student = Session.objects.filter(student = request.user, student_proposal = '0', tutor_proposal = '2').order_by('-start_date_and_time')
        waiting_acceptance_reject_tutor = Session.objects.filter(tutor = request.user, student_proposal = '2', tutor_proposal = '0').order_by('-start_date_and_time')
        
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
                
            average_rating = round(current_rating_sum/ current_num_ratings,2)
        else:
            average_rating = 0
            current_num_ratings = 0

        
        context_objects = {
            'user' : user,
            'accepted_student_sessions_future': accepted_student_sessions_future,
            'accepted_tutor_sessions_future' : accepted_tutor_sessions_future,
            'accepted_student_sessions_past': accepted_student_sessions_past,
            'accepted_tutor_sessions_past' : accepted_tutor_sessions_past,
            'pending_sessions_requested_student' :pending_sessions_requested_student, 
            'pending_sessions_requested_tutor' : pending_sessions_requested_tutor, 
            'waiting_acceptance_reject_student' : waiting_acceptance_reject_student,
            'waiting_acceptance_reject_tutor' : waiting_acceptance_reject_tutor,
            'classes_need_help_in' : classes_need_help_in,
            'classes_can_tutor_in' : classes_can_tutor_in,
            'reviews_received' : reviews_received,
            'reviews_written' : reviews_written,
            'average_rating' : average_rating,
            'ratings_received' : current_num_ratings,
            'form': EditProfileForm(request.POST),
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

        return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClassNeedsHelpForm()
        
    return render(request, 'QuickTutor/ClassNeedsHelpForm.html', {'form': form})

def Add_Tutorable_Class(request):

    form = TutorableClassForm(request.POST)

    if form.is_valid():
        new_class_can_tutor = form.save(commit=False)
        new_class_can_tutor.user = request.user
        new_class_can_tutor.save()

        return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TutorableClassForm()
        
    return render(request, 'QuickTutor/TutorableClassForm.html', {'form': form})

def Add_Review_Class(request):
    # if this is a POST request we need to process the form data
    form = ReviewForm(request.user, request.POST)

    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.Author = request.user
        new_review.time_of_review = datetime.datetime.now()
        new_review.save()

        return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReviewForm(request.user)
        
    return render(request, 'QuickTutor/ReviewForm.html', {'form': form})

def Create_Session(request):
    # if this is a POST request we need to process the form data
    form = CreateSessionForm(request.user, request.POST)
    userObject = QTUser.objects.get(username = request.user.username)
    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        date = form.cleaned_data['date']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']

        # date_formatted = dateparse.parse_date(date)
        format_ = '%I:%M %p'
        start_time_formatted = datetime.datetime.strptime(start_time,format_)
        end_time_formatted = datetime.datetime.strptime(end_time,format_)
        
        year = date.year
        month = date.month
        day = date.day
        start_hour = start_time_formatted.hour
        start_minute = start_time_formatted.minute
        end_hour = end_time_formatted.hour
        end_minute = end_time_formatted.minute

        start_comparison = datetime.datetime(year,month,day,start_hour,start_minute)

        if ((date.date() < datetime.datetime.today().date()) | (start_time_formatted >= end_time_formatted) | ((start_comparison.time() < datetime.datetime.today().time()) & (start_comparison.date() < datetime.datetime.today().date()))):
            #
            msg = "Please enter a valid date and time"
            return render(request, 'QuickTutor/create_session.html', {'form': form, "msg": msg})

        else:
            new_session = form.save(commit = False)
            new_session.student = request.user
            new_session.start_date_and_time = datetime.datetime(year,month,day,start_hour,start_minute)
            new_session.end_date_and_time = datetime.datetime(year, month, day, end_hour, end_minute)
            new_session.student_proposal = '2'
            new_session.save()

            subject = "Tutor Request [DO NOT REPLY]"
            message = 'You have a new request from ' + str(request.user.first_name) + ' ' + str(request.user.last_name) + ". If you would like to follow up with your student you can accept the session and email them about when to meet at Clemmons 2.\n Student Email: " + str(request.user.email) +  "\n Hourly Rate: $" + str(new_session.price_of_tutor) + " per hour" + "\n Link to application: https://quick-tutor-qtie5.herokuapp.com/" 
            recepient = new_session.tutor.email

            email = EmailMessage(subject, message, request.user.email ,[recepient], [request.user.email], reply_to=[request.user.email])
            email.send()
            return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateSessionForm(request.user)
        

    return render(request, 'QuickTutor/create_session.html', {'form': form})

def deleteSession(request, session_id):
    session = get_object_or_404(Session, pk = session_id)
    session.delete()

    return HttpResponseRedirect('/profile')

def deleteClassNeedsHelp(request, class_needs_help_id):
    class_needs_help = get_object_or_404(ClassNeedsHelp, pk = class_needs_help_id)
    class_needs_help.delete()
    
    return HttpResponseRedirect('/profile')

def rejectOffer(request, session_id):
    session = get_object_or_404(Session, pk = session_id)
    tutor = session.tutor
    student = session.student
    if session.tutor_proposal == "2": #When the student clicks the button
        subject = "Offer Rejected [DO NOT REPLY]"
        message = student.first_name + " " + student.last_name + " has rejected your offer"
        send_mail(subject, message, request.user.email ,[tutor.email], fail_silently = False)
    elif session.student_proposal == "2": #When the tutor clicks the button
        subject = "Offer Rejected [DO NOT REPLY]"
        message = tutor.first_name + " " + tutor.last_name + " has rejected your offer"
        send_mail(subject, message, request.user.email ,[student.email], fail_silently = False)
    session.delete()
    return HttpResponseRedirect('/profile')

def acceptOffer(request, session_id):
    session = get_object_or_404(Session, pk = session_id)
    tutor = session.tutor
    student = session.student
    if session.tutor_proposal == "0":
        session.tutor_proposal = "2"
        subject = "Offer Accepted [DO NOT REPLY]"
        message = tutor.first_name + " " + tutor.last_name + " has accepted your offer!"
        send_mail(subject, message, request.user.email ,[student.email], fail_silently = False)
    elif session.student_proposal == "0":
        session.student_proposal = "2"
        subject = "Offer Accepted [DO NOT REPLY]"
        message = student.first_name + " " + student.last_name + " has accepted your offer!"
        send_mail(subject, message, request.user.email ,[tutor.email], fail_silently = False)
    session.save()
    return HttpResponseRedirect('/profile')

def deleteTutorableClass(request, tutorable_class_id):
    tutorable_class = get_object_or_404(TutorableClass, pk = tutorable_class_id)
    tutorable_class.delete()
    
    return HttpResponseRedirect('/profile')

class SearchResultsView(generic.ListView):
    model = TutorableClass
    template_name = 'search_results.html'

class SearchPageView(generic.TemplateView):
    template_name = "QuickTutor/search.html"

    def get(self,request):
        user = request.user
        
        classes_need_help_in = list(ClassNeedsHelp.objects.filter(user = user))
        class_ids = ClassNeedsHelp.objects.filter(user = user).values('class_id')
        tutors_and_classes = list(TutorableClass.objects.filter(class_id__in=class_ids ))

        # for c in classes_need_help_in:
        #     tutors_and_classes.append(list(TutorableClass.objects.filter(class_id = c.class_id)))
        #     print('Class:', c, 'ID:', c.class_id )

        context_objects = {
            'classes_need_help_in' : classes_need_help_in,
            'tutors_and_classes' : tutors_and_classes,
        }
        return render(request, self.template_name, context = context_objects)

def OtherProfileView(request, user_id):
    template_name = 'QuickTutor/otherProfile.html'
    user = get_object_or_404(QTUser, pk= user_id)


    #classes need help in/can tutor in 
    classes_can_tutor_in = list(TutorableClass.objects.filter(user = user))

    #reviews
    reviews_received = list(Review.objects.filter(Recipient = user).order_by('-time_of_review'))

    average_rating = list(Review.objects.filter(Recipient = user).values('rating')) #returns dictionary
    if (len(average_rating) != 0):
        current_rating_sum = 0
        current_num_ratings = 0
        for rating in average_rating:
            current_rating_sum += rating['rating']
            current_num_ratings += 1
            
        average_rating = round(current_rating_sum/ current_num_ratings,2)
    else:
        average_rating = 0
        current_num_ratings = 0


    context_objects = {
        'user' : user,
        'classes_can_tutor_in' : classes_can_tutor_in,
        'reviews_received' : reviews_received,
        'average_rating' : average_rating,
        'ratings_received' : current_num_ratings
    }
    return render(request, template_name, context = context_objects)

def createSessionSpecific(request, tutor_id):
    #filters classes by ones that tutor can tutor in
    form = CreateSpecificSessionForm(tutor_id,request.POST)
    userObject = QTUser.objects.get(username = request.user.username)
    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        date = form.cleaned_data['date']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        subject_in_regards_to = form.cleaned_data['subject_in_regards_to']
        print("THIS WAT IT ABOUT", subject_in_regards_to)

        # date_formatted = dateparse.parse_date(date)
        format_ = '%I:%M %p'
        start_time_formatted = datetime.datetime.strptime(start_time,format_)
        end_time_formatted = datetime.datetime.strptime(end_time,format_)
        
        year = date.year
        month = date.month
        day = date.day
        start_hour = start_time_formatted.hour
        start_minute = start_time_formatted.minute
        end_hour = end_time_formatted.hour
        end_minute = end_time_formatted.minute

        start_comparison = datetime.datetime(year,month,day,start_hour,start_minute)

        if ((date.date() < datetime.datetime.today().date()) | (start_time_formatted >= end_time_formatted) | ((start_comparison.time() < datetime.datetime.today().time()) & (start_comparison.date() < datetime.datetime.today().date()))):
            print(start_time_formatted, end_time_formatted, start_time_formatted >= end_time_formatted)
            msg = "Please enter a valid date and time"
            return render(request, 'QuickTutor/create_session.html', {'form': form, "msg" : msg})
        else:
            new_session = form.save(commit = False)
            new_session.student = request.user
            new_session.tutor = get_object_or_404(QTUser, pk=tutor_id)
            new_session.start_date_and_time = datetime.datetime(year,month,day,start_hour,start_minute)
            new_session.end_date_and_time = datetime.datetime(year, month, day, end_hour, end_minute)
            new_session.student_proposal = '2'
            new_session.price_of_tutor = form.cleaned_data["price_of_tutor"]
            new_session.save()


            subject = "Tutor Request [DO NOT REPLY]"
            message = 'You have a new request from ' + str(request.user.first_name) + ' ' + str(request.user.last_name) + " for a tutoring session in " + str(subject_in_regards_to) + ". If you would like to follow up with your student you can accept the session and email them about when to meet at Clemmons 2.\n Student Email: " + str(request.user.email) +  "\n Hourly Rate: $" + str(new_session.price_of_tutor) + " per hour" + "\n Link to application: https://quick-tutor-qtie5.herokuapp.com/" 
            recepient = new_session.tutor.email

            email = EmailMessage(subject, message, request.user.email ,[recepient], [request.user.email], reply_to=[request.user.email])
            email.send()
            return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateSpecificSessionForm(tutor_id)
        

    return render(request, 'QuickTutor/create_session.html', {'form': form})

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

        return HttpResponseRedirect('/profile/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditProfileForm()
        
    return render(request, 'QuickTutor/editProfile.html', {'form': form})