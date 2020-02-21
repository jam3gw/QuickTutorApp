from django.shortcuts import render
from django.http import HttpResponse
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordResetView

def index(request):
    return render(request, 'QuickTutor/homepage.html', {})
# Create your views here.
    