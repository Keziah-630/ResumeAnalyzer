from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileForm
from .admin_forms import RegularUserAuthenticationForm, AdminAuthenticationForm
from .password_forms import ForgotPasswordForm, VerificationForm, ResetPasswordForm
from django.contrib.auth.models import User
from resumes.models import Resume
import random
import string
from django.core.mail import send_mail

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Auto-login after registration
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
                return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = RegularUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Clear any existing session data
                request.session.flush()
                
                # Login the user
                login(request, user)
                
                # Set session data for regular user
                request.session['user_type'] = 'regular'
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('home')
        else:
            # Handle form errors with specific messages
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_name = field.replace('_', ' ').title()
                        messages.error(request, f"{field_name}: {error}")
    else:
        form = RegularUserAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def admin_login_view(request):
    """Separate admin login view"""
    if request.method == 'POST':
        form = AdminAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the admin user
            user = authenticate(username=username, password=password)
            if user is not None and (user.is_superuser or user.is_staff):
                # Clear any existing session data
                request.session.flush()
                
                # Login the admin user
                login(request, user)
                
                # Set session data for admin user
                request.session['user_type'] = 'admin'
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                
                messages.success(request, f'Welcome to admin panel, {user.username}!')
                return redirect('/admin/')
        else:
            # Handle form errors with specific messages
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_name = field.replace('_', ' ').title()
                        messages.error(request, f"{field_name}: {error}")
    else:
        form = AdminAuthenticationForm()
    
    return render(request, 'users/admin_login.html', {'form': form})

def forgot_password_view(request):
    """Handle forgot password request"""
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            verification_method = form.cleaned_data.get('verification_method')
            try:
                user = User.objects.get(username=username)
                # Generate verification code
                verification_code = ''.join(random.choices(string.digits, k=6))
                # Store verification code in session
                request.session['reset_username'] = username
                request.session['verification_code'] = verification_code
                request.session['verification_method'] = verification_method
                # Send code via email
                if verification_method == 'email':
                    send_mail(
                        'Your Resume Analyzer Verification Code',
                        f'Your verification code is: {verification_code}',
                        None,  # Uses DEFAULT_FROM_EMAIL
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, f'Verification code sent to {user.email}.')
                    messages.info(request, f'📧 Email: {user.email}')
                else:
                    # Get phone from resume if available
                    try:
                        resume = Resume.objects.get(user=user)
                        phone = resume.phone
                    except Resume.DoesNotExist:
                        phone = 'Phone number not available'
                    # For SMS, you would integrate with an SMS API here
                    messages.success(request, f'Verification code sent via SMS.')
                    messages.info(request, f'📱 Phone: {phone}')
                return redirect('verify_code')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_name = field.replace('_', ' ').title()
                        messages.error(request, f"{field_name}: {error}")
    else:
        form = ForgotPasswordForm()
    return render(request, 'users/forgot_password.html', {'form': form})

def verify_code_view(request):
    """Handle verification code"""
    if 'reset_username' not in request.session:
        messages.error(request, 'Please start the password reset process.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data.get('verification_code')
            stored_code = request.session.get('verification_code')
            
            if verification_code == stored_code:
                messages.success(request, 'Verification successful! Please set your new password.')
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = VerificationForm()
    
    return render(request, 'users/verify_code.html', {'form': form})

def reset_password_view(request):
    """Handle password reset"""
    if 'reset_username' not in request.session:
        messages.error(request, 'Please start the password reset process.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            username = request.session.get('reset_username')
            
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                
                # Clear session data
                del request.session['reset_username']
                del request.session['verification_code']
                del request.session['verification_method']
                
                messages.success(request, 'Password reset successful! Please login with your new password.')
                return redirect('login')
                
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_name = field.replace('_', ' ').title()
                        messages.error(request, f"{field_name}: {error}")
    else:
        form = ResetPasswordForm()
    
    return render(request, 'users/reset_password.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})
