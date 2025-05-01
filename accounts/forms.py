from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' , 'first_name', 'last_name', 'email', 'password1', 'password2']
        
        # widgets = {                                  # the class name is in my css file
        #     'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name', 'required': 'required'}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        # }
        
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat the password'}),
        }
        
        
