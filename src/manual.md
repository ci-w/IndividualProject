# User manual 
Describe how to use your software, if this makes sense for your code. Almost all projects should have at least some instructions on how to run the code. More extensive instructions can be provided here.

## Requirements
uses pip: install pip 

uses anaconda virtual env: <br>
To create a conda virtualenv in the current dir use: <br>
`$ conda create --prefix=yourEnvName python=3.8` <br>
To delete a conda env: <br>
`$ conda env remove `

Then activate virtual env and install: <br>
`pip install django==3.2.16` <br>
`pip install pillow`

Creating a django project: <br>
`django-admin startproject tango_with_django_project . `

Creating a django app: <br>
` src into django project dir ` <br>
`python manage.py startapp appname ` <br>
Then add this app to your django projects installed apps list in its settings file <br>

Running a server: (while in src folder) <br>
`python manage.py runserver`

Pipe environment requirements to file: <br>
`conda list > requirements.txt` <br>
Creating project from this: <br>
`pip install -r requirements.txt` <br>

Population script 
` python populate_making.py ` 

Changing models 
` python manage.py makemigrations making ` <br>
` python manage.py migrate `
If you delete the database, have to make a new superuser account:
` python manage.py createsuperuser `

To interact with Django models directly through shell: <br>
`python manage.py shell`
`import making.models`

View underlying SQL for specified django migration:
`python manage.py sqlmigrate making 0001`

## GIT
Removing folder from remote repo that's now in gitingore: <br>
`git rm -r --cached some-directory` <br>
`git commit -m 'Remove the now ignored directory "some-directory"'`<br>
`git push origin main` <br>

## Notes
To format nicely in vsc: shift alt f <br>
To format (soft) line wrapping: alt z <br>
Potential hosting sites: pythonanywhere & surge <br>

To get django site to run on local: <br>
open anaconda prompt <br>
`conda activate makingenv` <br>
cd into src directory <br>
`python manage.py runserver`

## Population
Structure of JSON file is: [Project] [Project's requirements] [Project's tools] for all projects, then [User] [User's profiles] [User's profiles requirements] [User profiles tools] for all users should create User's in admin interface, dump to file, then copy paste them in there.

To load in data from fixture:
python manage.py loaddata test.json
where test.json is in the app's fixtures folder

## PythonAnywhere
If you change any static files need to run:
python manage.py collectstatic

## Secret key / dotenv
Using this to keep the secret key a secret when hosting site. 
Do so by using environment variables. 
State them in a file `.env` in the main dir. 
`export SECRET_KEY="keyvalue" `
Then have to install python-dotenv to run this file. If using a virtual environment, install through that process:
`conda install python-dotenv` 
Otherwise:
`pipX.Y install --user python-dotenv `
where X.Y is the python version you're using. 

Then need to load in this value to your wgsi file. Need to put this before the code that runs the website (i.e. `get_wsgi_application`):
`from dotenv import load_dotenv` 
`load_dotenv(os.path.join(PROJECT_PATH, '.env'))` 
Then modify settings.py to use this environment variable:
`SECRET_KEY = os.getenv("SECRET_KEY")`

To generate a new secret key using Djangos functions:
` from django.core.management.utils import get_random_secret_key`
` print(get_random_secret_key()) `


## Django notes
If you're accessing a dictionary in a template, don't use dict_name['key'] to get that keys value, it doesn't work. You can instead use dot notation: dict_name.key will work. 