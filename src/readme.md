# Readme
Making Projects Django project. 

## Build Instructions

### Requirements
* Python 3.8 
* Django 4.1.6
* SQLite 3.41.1
* Packages listed in `requirements.txt`
* Tested on Windows 11 

### Build steps 
It is advised to use a virtual environment. 

Clone repository to local machine, cd to src directory. 
Activate virtual environment, if you are using one. 

Using pip:

` pip install -r requirements.txt ` 


Set up secret key: 

Create a file named `.env` in the src directory. 

Within it:

` export SECRET_KEY='key_here' `

where key_here is your secret key (usually a random combination of symbols)


Then to run site on local machine (127.0.0.1:8000/):

`python manage.py runserver`  

