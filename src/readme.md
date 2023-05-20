# Making Projects
1 line description - Making Projects Django project. 

<img src="../dissertation/images/syllabus.png">


* Python 3.8 
* Django 4.1.6
* SQLite 3.41.1
* Packages listed in `requirements.txt`

Tested on Windows 11 
____________________________________
## Build Instructions
How to start running a local version of Making Projects. 

### Prerequisites 
* Python 3.8
* pip

### Build Steps 
It is advised to use a virtual environment. 

1. Clone the repository
``` ssh
git clone https://github.com/ci-w/IndividualProject.git
```
2. Navigate to src directory
```
cd src
```

3. Use pip to install packages

```
pip install -r requirements.txt
``` 
4. Generate a Django secret key (50 random characters) at https://djecrety.ir/ (alternative: https://django-secret-key-generator.netlify.app/)
5. Create a file named `.env` in the src directory
6. Write within it, where `key_here` is your secret key
```
export SECRET_KEY='key_here'
```
7. To run local development server (127.0.0.1:8000/)
```
python manage.py runserver
```
____________________________________