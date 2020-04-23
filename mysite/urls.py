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
    # path('login/',TemplateView.as_view(template_name="login/loginPage.html")),
    path('aboutus/',TemplateView.as_view(template_name="QuickTutor/aboutus.html")),
    path('profile/', ProfileView.as_view()),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('feedback/', include('QuickTutor.urls')),
    path('profile/add-class-needs-help/', Add_Class_Needs_Help),
    path('profile/add-tutorable-class/', Add_Tutorable_Class),
    path('profile/add-review/', Add_Review_Class),
    path('profile/edit-profile/', edit_Profile_Class),
    path('profile/view-reviews/', ReviewsView.as_view()),
    path('profile/new-session/', Create_Session),
    path('profile/new-session/<tutor_id>', createSessionSpecific, name = "specific_session_creation"),
    path('profile/delete_session/<session_id>/', deleteSession, name= "delete_session"),
    path('profile/delete_class_needs_help/<class_needs_help_id>/', deleteClassNeedsHelp, name= "delete_class_needs_help"),
    path('profile/delete_tutorable_class/<tutorable_class_id>/', deleteTutorableClass, name= "delete_tutorable_class"),
    path('profile/reject_session/<session_id>/', rejectOffer, name="reject_session"),
    path('profile/accept_session/<session_id>/', acceptOffer, name="accept_session"),
    path('search/', SearchPageView.as_view()),
    # path('search-results/', TemplateView.as_view(template_name="QuickTutor/search_results.html")),
    path('search/<user_id>/', OtherProfileView, name="other_profile")

]
