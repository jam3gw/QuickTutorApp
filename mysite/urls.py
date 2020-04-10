"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.views.generic import TemplateView, ListView, DetailView
from QuickTutor.views import *

urlpatterns = [
    path('',TemplateView.as_view(template_name="QuickTutor/index.html")),
    path('login/',TemplateView.as_view(template_name="login/loginPage.html")),
    path('aboutus/',TemplateView.as_view(template_name="QuickTutor/aboutus.html")),
    path('profile/', ProfileView.as_view()),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('feedback/', include('QuickTutor.urls')),
    path('profile/add-class-needs-help/', Add_Class_Needs_Help),
    path('profile/add-tutorable-class/', Add_Tutorable_Class),
    path('profile/add-review/', Add_Review_Class),
    path('profile/view-reviews/', ReviewsView.as_view()),
    path('profile/view-sessions/', SessionsView.as_view()),
    path('profile/view-sessions/new-session/', Create_Session),
    path('profile/edit-profile/', edit_Profile_Class),
    path('sessions/success/', TemplateView.as_view(template_name="QuickTutor/success.html"))
]
