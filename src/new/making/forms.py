from django.forms import ModelForm, Form
from making.models import Requirements, Tool, UserProfile
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django import forms

# can i use this for both registering and logging in?
# change behaviour cos its saying stuff abt registering
class UserForm(ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.EmailField(max_length=64,
                                help_text="The person's email address.")
    class Meta:
        model = User
        fields = ('username', 'password',)

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_name',)

class RequirementsForm(ModelForm):
    '''vision = forms.IntegerField(required=False)
    dexterity = forms.IntegerField(required=False)
    language = forms.IntegerField(required=False)
    memory = forms.IntegerField(required=False)'''
    class Meta:
        model = Requirements
        fields = '__all__'

class ToolForm(ModelForm):
    #name = forms.CharField(max_length=64, required=False)
    #skill_level = forms.IntegerField(required=False)
    class Meta:
        model = Tool
        fields = ('name', 'skill_level',)

#todo: make it so you select a project, and the form just punts through the project ID. i.e. have to do validation here
class SyllabusForm(Form):
    end_project = forms.IntegerField()
