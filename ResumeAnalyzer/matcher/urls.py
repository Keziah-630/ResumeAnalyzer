from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_matches, name='job_matches'),
    path('<int:match_id>/', views.match_detail, name='match_detail'),
    path('<int:match_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:match_id>/apply/', views.apply_from_match, name='apply_from_match'),
    path('preferences/', views.match_preferences, name='match_preferences'),
    path('history/', views.match_history, name='match_history'),
] 