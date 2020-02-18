# project-103-qtie5

## Installation notes for setting up Postgres
### Create the database 
To create the Postgres databse, run the following commands in your terminal:
````
 psql postgres -c "CREATE USER qtie5 WITH PASSWORD 'password';"
 psql postgres -c "CREATE DATABASE quicktutordb WITH OWNER qtie5;"
psql postgres -c "ALTER USER qtie5 SUPERUSER CREATEROLE CREATEDB REPLICATION;"
````

### Create the database superuser

To access the database through the django admin portal, run the following command in your terminal 

````
python3 manage.py createsuperuser
```` 
It will then prompt you to enter user credentials. You can then use these credentials to log into the admin portal.


## Installation notes for deploying on Heroku:
- In order to run Google OAuth on your local server you need to run the following commands in your terminal:
    pip3 install django-allauth
    pip3 install social-auth-app-django
- Create a superuser for the Heroku account so we can be an admin on the site 
- In the admin, configure the Google OAuth Client ID and Secret Key with the Site Authorization on the Heroku admin page
- Go to this website: https://console.developers.google.com/apis/credentials/oauthclient/209060647268-2gma3tapsd6qkqcdodv9p0jv26ig9raq.apps.googleusercontent.com?project=quick-tutor-268316 and configure the page at which the login will occur on Heroku as well as the redirect page after the login is successful
- Go to the sites and add the Google login (via this tutorial: https://www.youtube.com/watch?v=ZTBexYIIOP8) via the admin part of the webapp