from django.forms import ModelForm, Form
from making.models import Requirements, Tool, UserProfile, Project
from django.contrib.auth.models import User
from django import forms

# can i use this for both registering and logging in?
# change behaviour cos its saying stuff abt registering
class UserForm(ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.EmailField(max_length=64, label="Email")
    class Meta:
        model = User
        fields = ('username', 'password',)

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_name',)

class RequirementsForm(ModelForm):
    class Meta:
        model = Requirements
        fields = '__all__'

class ToolForm(ModelForm):
    name = forms.ChoiceField()
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