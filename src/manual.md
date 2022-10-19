# User manual 

Describe how to use your software, if this makes sense for your code. Almost all projects should have at least some instructions on how to run the code. More extensive instructions can be provided here.

uses pip: install pip 
uses anaconda virtual env:
To create a conda virtualenv in the current dir use:
$ conda create --prefix=yourEnvName python=3.8
To delete a conda env:
$ conda env remove 

Then activate virtual env and do:
install within virtual environment:
pip install django==3.2.16
pip install pillow

Creating a django project:
django-admin startproject tango_with_django_project . 

Running a server: (while in src folder)
python manage.py runserver

Pipe enviroment requirements to file:
conda list > requirements.txt

