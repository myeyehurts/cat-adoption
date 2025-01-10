from django import forms
from django.contrib.auth.forms import UserCreationForm

from catadoption.models import AdoptionProfile, ModifiedUser

class RegistrationForm(UserCreationForm):
    # uses the modified user model
    class Meta:
        model = ModifiedUser
        fields = ('username', 'email', 'password1', 'password2', 'profile_pic')
        labels = {
            'profile_pic': 'Profile picture'
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AdoptionProfileForm(forms.ModelForm):
    # uses the AdoptionProfile model aside from user field which is already defined
    class Meta:
        model = AdoptionProfile
        exclude = ['user']
        # adding more comprehensive text to display for these fields
        labels = {
            'date_of_birth': 'Date of birth (yyyy-mm-dd)',
            'has_children': 'There are children in my household.',
            'has_pets': 'There are pets in my household.',
            'has_allergies': 'I am allergic to cats.',
            'special_needs_pref': 'I am okay with a cat that has special needs.',
            'several_cats_pref': 'I am open to adopting more than one cat.'
        }