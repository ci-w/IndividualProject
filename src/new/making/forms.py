from django.forms import ModelForm, Form
from making.models import Requirements, Tool, UserProfile, Project
from django.contrib.auth.models import User
from django import forms
from django.forms import formset_factory

# can i use this for both registering and logging in?
# change behaviour cos its saying stuff abt registering
class UserForm(ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.EmailField(max_length=64, label="Email")
    class Meta:
        model = User
        fields = ('username', 'password',)

# cant use the model form for logging in because Django assumes you are registering a new user every time
class LoginForm(Form):
    username = forms.EmailField(max_length=64, label="Email")
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_name',)

class RequirementsForm(ModelForm):
    class Meta:
        model = Requirements
        fields = '__all__'

# name choices are just every tool thats been used in a project
class ToolForm(ModelForm):
    CHOICES = Tool.choices_objects.get_choices
    name = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Tool
        fields = ('name','skill_level',)

class SyllabusForm(Form):
    # get all project ID's and titles
    CHOICES = Project.choices_objects.get_choices()
    end_project = forms.ChoiceField(choices=CHOICES)

class SwitchProfileForm(Form):
    #the choices are decided in the View because it depends on the User
    profile = forms.ChoiceField()