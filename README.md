# project-103-qtie5

Installation notes for deploying on Heroku:
- In order to run Google OAuth on your local server you need to run the following commands in your terminal:
    pip3 install django-allauth
    pip3 install social-auth-app-django
- Create a superuser for the Heroku account so we can be an admin on the site 
- In the admin, configure the Google OAuth Client ID and Secret Key with the Site Authorization on the Heroku admin page
- Go to the sites 