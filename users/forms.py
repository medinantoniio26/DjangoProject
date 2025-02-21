from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password = forms.CharField(widget=forms.PasswordInput()) 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    username = forms.CharField(required=False)  # Evita validación en blanco al inicio
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=True)
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 
   
