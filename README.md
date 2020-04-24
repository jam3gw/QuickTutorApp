# project-103-qtie5
# Acknowledgements 
## Django
[Django](https://www.djangoproject.com/start/overview/) is owned by the [Django Software Foundation](https://www.djangoproject.com/foundation/), and is released under the [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://creativecommons.org/licenses/by-sa/3.0/).

## Postgres
Used for the database. Used under the PostgresQL Liscence. Learn more [here](https://www.postgresql.org/about/licence/).

## Twillio
[Twillio](https://www.twilio.com/docs) was used under the free student account. 

# Developer Notes
## Installation notes for setting up Postgres
### Start postgres
#### For Mac Users:
If you haven't already, run 
````
brew services start postgres
````
#### For windows users: 
Idk how to start postgres on windows. Google it, I guess. w

### Create the database 
To create the Postgres databse, run the following commands in your terminal:
````
psql postgres -c "CREATE USER qtie5 WITH PASSWORD 'password';"
psql postgres -c "CREATE DATABASE quicktutordb WITH OWNER qtie5;"
psql postgres -c "ALTER USER qtie5 SUPERUSER CREATEROLE CREATEDB REPLICATION;"
````

## IF RECEIVING A PROGRAMMING ERROR:
deletion of postgres database if needed:
````psql postgres -c "drop database quicktutordb;"````
You then will need to re-run: 
````
psql postgres -c "CREATE DATABASE quicktutordb WITH OWNER qtie5;"
psql postgres -c "ALTER USER qtie5 SUPERUSER CREATEROLE CREATEDB REPLICATION;"
````

if you delete and re-make the database, remake the migrations BEFORE creation of the superuser 

### Migrate
Run these commands after deleting postgres and remaking the database.
````
python3 manage.py makemigrations
python3 manage.py migrate
````
### Re-populate classes
After restarting the database run 
````
python3 manage.py csvimport
````
to re-populate the database with classes

### Create the database superuser

To access the database through the django admin portal, run the following command in your terminal 
````
python3 manage.py createsuperuser
```` 
It will then prompt you to enter user credentials. You can then use these credentials to log into the admin portal.

## Restarting Postgres
````
brew services restart postgresql  
````

## Installation notes for deploying on Heroku:
- In order to run Google OAuth on your local server you need to run the following commands in your terminal:
    pip3 install django-allauth
- Create a superuser for the Heroku account so we can be an admin on the site 
- In the admin, configure the Google OAuth Client ID and Secret Key with the Site Authorization on the Heroku admin page
- Go to this website: https://console.developers.google.com/apis/credentials/oauthclient/209060647268-2gma3tapsd6qkqcdodv9p0jv26ig9raq.apps.googleusercontent.com?project=quick-tutor-268316 and configure the page at which the login will occur on Heroku as well as the redirect page after the login is successful
- Go to the sites and add the Google login (via this tutorial: https://www.youtube.com/watch?v=ZTBexYIIOP8) via the admin part of the webapp

# Class Data Format
The data used to populate the class database is stored in a CSV in the following format:
| CLASS_NAME                               	| DEPT 	| COURSE_NUM 	| COURSE_TOPIC                    	| FULL_ID                                                                 	|
|------------------------------------------	|------	|------------	|---------------------------------	|-------------------------------------------------------------------------	|
| Program and Data Representation          	| CS   	| 2150       	|                                 	| Program and Data RepresentationCS2150                                   	|
| Special Topics in Computer Science       	| CS   	| 3501       	| Foundations of Data Analysis    	| Special Topics in Computer ScienceCS3501Foundations of Data Analysis    	|
| Special Topics in Computer Science       	| CS   	| 3501       	| Embedded Computing & Robotics I 	| Special Topics in Computer ScienceCS3501Embedded Computing & Robotics I 	|
| Advanced Software Development Techniques 	| CS   	| 3240       	|                                 	| Advanced Software Development TechniquesCS3240                          	|

The FULL_ID field is a concatenation of all the previous fields in that row. In the class model, the `full_id` field is not null and must be unique. 