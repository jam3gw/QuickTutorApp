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
        if (len(Session.objects.filter(student = user)) != 0):
            student_sessions = Session.objects.filter(student = user).get()
        else : 
            student_sessions = 'None'

        if (len(Session.objects.filter(tutor = user)) != 0):
            tutor_sessions = Session.objects.filter(tutor = user).get()
        else : 
            tutor_sessions = 'None'

        #classes need help in/can tutor in 
        if (len(ClassNeedsHelp.objects.filter(user = user)) != 0 ):
            classes_need_help_in = ClassNeedsHelp.objects.filter(user = user).get()
        else: 
            classes_need_help_in = 'None'

        if (len(TutorableClass.objects.filter(user = user)) != 0):
            classes_can_tutor_in = TutorableClass.objects.filter(user = user).get()
        else:
            classes_can_tutor_in = 'None'

        #reviews
        if (len(Review.objects.filter(Recipient = user)) != 0):
            reviews_received = Review.objects.filter(Recipient = user).get()
        else:
            reviews_received = 'None'

        if (len(Review.objects.filter(Author = user)) != 0):
            reviews_written = Review.objects.filter(Author = user).get()
        else:
            reviews_written = 'None'

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
