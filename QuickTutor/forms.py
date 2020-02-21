# from allauth.account.forms import LoginForm, ResetPasswordForm, SignupForm
# from .models import QTUser

# class CustomSignupForm(SignupForm):
#     def signup(self, request, user):
#         # Ensure you call the parent class's save.
#         # .save() returns a User object.
#         user = super(CustomSignupForm, self).save()

#         # Add your own processing here.

#         # You must return the original result.
#         return user

# class CustomLoginForm(LoginForm):
#     def login(self):

#         # Add your own processing here.

#         # You must return the original result.
#         return super(CustomLoginForm, self).login()
