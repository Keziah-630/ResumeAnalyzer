from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
import re

class ForgotPasswordForm(forms.Form):
    """Form for initiating password reset"""
    
    VERIFICATION_CHOICES = [
        ('email', 'Email Address'),
        ('phone', 'Phone Number'),
    ]
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        }),
        error_messages={
            'required': 'Please enter your username.',
        }
    )
    
    verification_method = forms.ChoiceField(
        choices=VERIFICATION_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        initial='email',
        error_messages={
            'required': 'Please select a verification method.',
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
                    'Password reset for admin accounts is not available through this form. Please contact your system administrator.'
                )
        except User.DoesNotExist:
            raise forms.ValidationError('No user found with this username.')
        
        return username

class VerificationForm(forms.Form):
    """Form for verification code"""
    
    verification_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit code',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        }),
        error_messages={
            'required': 'Please enter the verification code.',
            'max_length': 'Verification code must be 6 digits.',
        }
    )
    
    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError('Please enter a valid 6-digit verification code.')
        return code

class ResetPasswordForm(forms.Form):
    """Form for setting new password"""
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        error_messages={
            'required': 'Please enter a new password.',
        }
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        error_messages={
            'required': 'Please confirm your new password.',
        }
    )
    
    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        if not password:
            raise forms.ValidationError('Please enter a new password.')
        
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        
        if not re.search(r"\d", password):
            raise forms.ValidationError('Password must contain at least one number.')
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError('Password must contain at least one special character.')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        
        return cleaned_data 