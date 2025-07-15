from django.urls import path
from . import views
from . import admin_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-code/', views.verify_code_view, name='verify_code'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-access/', views.admin_login_view, name='admin_access'),  # Hidden admin access
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('admin-redirect/', admin_views.admin_login_redirect, name='admin_redirect'),
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
]