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
Structure of JSON file is: [Project] [Project's requirements] [Project's tools] for all projects, then [User] [User's profiles] [User's profiles requirements] [User profiles tools] for all users should create User's in admin interface, dump to file, then copy paste them in there