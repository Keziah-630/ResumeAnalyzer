from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

def is_admin_user(user):
    """Check if user is admin (superuser or staff)"""
    return user.is_superuser or user.is_staff

@staff_member_required
def admin_dashboard(request):
    """Custom admin dashboard that sets proper session data"""
    if request.user.is_authenticated and is_admin_user(request.user):
        # Set admin session data
        request.session['user_type'] = 'admin'
        request.session['user_id'] = request.user.id
        request.session['username'] = request.user.username
        
        return render(request, 'users/admin_dashboard.html', {
            'user': request.user
        })
    else:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('/admin/')

def admin_login_redirect(request):
    """Redirect admin users to proper admin login"""
    if request.user.is_authenticated and is_admin_user(request.user):
        # Set admin session data
        request.session['user_type'] = 'admin'
        request.session['user_id'] = request.user.id
        request.session['username'] = request.user.username
        
        messages.info(request, f'Welcome to admin panel, {request.user.username}!')
        return redirect('/admin/')
    else:
        return redirect('/admin/') 