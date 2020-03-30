from django.shortcuts import render
from django.http import HttpResponse
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordResetView
from django.views import generic
from .models import QTUser
from django.http import JsonResponse
from django.conf import settings

from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
    SyncGrant,
    ChatGrant
)

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
    model = QTUser
    template_name = 'QuickTutor/profile.html'
    context_object_name = 'user' #This is the object that is referenced in the HTML script

    