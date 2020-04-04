from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordResetView
from django.views import generic
from .models import QTUser, Review, Session, Class, ClassNeedsHelp, TutorableClass
from .forms import ClassNeedsHelpForm, TutorableClassForm, SessionForm, ReviewForm

def index(request):
    return render(request, 'QuickTutor/index.html', {})
# Create your views here.

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