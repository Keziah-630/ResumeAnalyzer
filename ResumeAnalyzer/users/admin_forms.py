from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class AdminAuthenticationForm(AuthenticationForm):
    """Custom authentication form for admin users only"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter admin username'
        }),
        error_messages={
            'required': 'Please enter your admin username.',
            'invalid': 'Please enter a valid admin username.'
        }
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter admin password'
        }),
        error_messages={
            'required': 'Please enter your admin password.',
            'invalid': 'Please enter a valid password.'
        }
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Please enter your admin username.')
        
        try:
            user = User.objects.get(username=username)
            if not (user.is_superuser or user.is_staff):
                raise forms.ValidationError(
                    'This account does not have administrative privileges. Please use the regular user login.'
                )
        except User.DoesNotExist:
            raise forms.ValidationError(
                'No admin user found with this username. Please check your credentials.'
            )
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(
                    'Invalid admin credentials. Please check your username and password.'
                )
            elif not (user.is_superuser or user.is_staff):
                raise forms.ValidationError(
                    'This account does not have administrative privileges.'
                )
        
        return cleaned_data

class RegularUserAuthenticationForm(AuthenticationForm):
    """Custom authentication form for regular users only"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        }),
        error_messages={
            'required': 'Please enter your username.',
            'invalid': 'Please enter a valid username.'
        }
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        error_messages={
            'required': 'Please enter your password.',
            'invalid': 'Please enter a valid password.'
        }
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Please enter your username.')
        
        try:
            user = User.objects.get(username=username)
            if user.is_superuser or user.is_staff:
                raise forms.ValidationError(
                    'This account is for administrative use only. Please contact your system administrator.'
                )
        except User.DoesNotExist:
            # Don't reveal if user exists or not for security
            pass
        
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(
                    'Invalid username or password. Please check your credentials.'
                )
            elif user.is_superuser or user.is_staff:
                raise forms.ValidationError(
                    'This account is for administrative use only.'
                )
        
        return cleaned_data 