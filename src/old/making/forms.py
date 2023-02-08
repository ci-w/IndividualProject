from django import forms
from django.contrib.auth.models import User
from making.models import UserProfile

class UserForm(forms.ModelForm):
    # hides password
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('requirements', )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('has_3D_printer', 'dexterity_level', 'instruction_level')