from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

class UserSessionMiddleware(MiddlewareMixin):
    """
    Middleware to handle session separation between admin and regular users.
    Prevents admin users from accessing regular user areas and vice versa.
    """
    
    def process_request(self, request):
        if not request.user.is_authenticated:
            return None
            
        # Get the current path
        current_path = request.path
        
        # Define admin paths - Django's built-in admin and custom admin routes
        admin_paths = ['/admin/', '/admin', '/users/admin-login/', '/users/admin-access/']
        
        # Check if user is admin (superuser or staff)
        is_admin_user = request.user.is_superuser or request.user.is_staff
        
        # If user is regular user and trying to access admin areas
        if not is_admin_user and any(current_path.startswith(path) for path in admin_paths):
            # Redirect regular users away from admin
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('/')
        
        # Don't redirect admin users away from regular areas - let them access both
        # This allows admin users to use the regular interface if needed
        
        return None

class SessionProtectionMiddleware(MiddlewareMixin):
    """
    Middleware to protect user sessions from being hijacked by admin sessions.
    """
    
    def process_request(self, request):
        if not request.user.is_authenticated:
            return None
            
        # Store user type in session for tracking
        if not hasattr(request, 'session'):
            return None
            
        current_user_type = 'admin' if (request.user.is_superuser or request.user.is_staff) else 'regular'
        
        # Check if session user type matches current user type
        session_user_type = request.session.get('user_type')
        
        if session_user_type and session_user_type != current_user_type:
            # Session mismatch detected - clear session and redirect
            request.session.flush()
            messages.error(request, 'Session conflict detected. Please login again.')
            return redirect('/users/login/')
        
        # Update session with current user type
        request.session['user_type'] = current_user_type
        request.session['user_id'] = request.user.id
        
        return None 