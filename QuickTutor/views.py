from django.shortcuts import render
from django.http import HttpResponse
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordResetView
from django.views import generic
from .models import QTUser, Review, Session, Class, ClassNeedsHelp, TutorableClass

def index(request):
    return render(request, 'QuickTutor/index.html', {})
# Create your views here.

class ProfileView(generic.TemplateView):
    template_name = 'QuickTutor/profile.html'

    def get(self,request):
        user = request.user

        #sessions participated in 
        student_sessions = Session.objects.filter(student = user)
        tutor_sessions = Session.objects.filter(tutor = user)

        #classes need help in/can tutor in 
        classes_need_help_in = ClassNeedsHelp.objects.filter(user = user)
        classes_can_tutor_in = TutorableClass.objects.filter(user = user)

        #reviews
        reviews_received = Review.objects.filter(Recipient = user)
        reviews_written = Review.objects.filter(Author = user)

        context_objects = {
            'user' : user,
            'student_sessions': student_sessions,
            'tutor_sessions' : tutor_sessions,
            'classes_need_help_in' : classes_need_help_in,
            'classes_can_tutor_in' : classes_can_tutor_in,
            'reviews_received' : reviews_received,
            'reviews_written' : reviews_written
        }
        return render(request, self.template_name, context = context_objects)
