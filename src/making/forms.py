from django.forms import ModelForm, Form, BaseFormSet
from making.models import Requirements, Tool, UserProfile, Project
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms 

# for registering
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

# name choices are just every tool that's been used in a project
class ToolForm(ModelForm):
    CHOICES = Tool.choices_objects.get_choices
    name = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Tool
        fields = ('name','skill_level')

class SyllabusForm(Form):
    # get all project ID's and titles
    CHOICES = Project.choices_objects.get_choices()
    end_project = forms.ChoiceField(choices=CHOICES)

class SwitchProfileForm(Form):
    #the choices are decided in the View because it depends on the user profile
    profile = forms.ChoiceField()

# tool formset validation 
class BaseToolFormSet(BaseFormSet):
    # checks no tools have the same name
    def clean(self):
        # dont bother unless each form is valid on its own
        if any(self.errors):
            return 
        names = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            name = form.cleaned_data.get('name')
            if name in names:
                raise ValidationError("Cannot add same tool twice.")
            names.append(name)