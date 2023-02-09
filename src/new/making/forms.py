from django.forms import ModelForm
from making.models import Requirements, Tool
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

# can i use this for both registering and logging in?
class UserForm(ModelForm):  
    class Meta:
        model = User
        fields = ('username', 'password',)

class RequirementsForm(ModelForm):
    class Meta:
        model = Requirements
        fields = '__all__'

class ToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = '__all__'