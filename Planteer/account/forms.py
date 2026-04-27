from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about','avatar']

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

