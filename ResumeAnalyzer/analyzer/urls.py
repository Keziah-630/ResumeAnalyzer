from django.urls import path
from . import views

urlpatterns = [
    path('', views.analysis_list, name='analysis_list'),
    path('<int:resume_id>/analyze/', views.analyze_resume, name='analyze_resume'),
    path('<int:resume_id>/detail/', views.analysis_detail, name='analysis_detail'),
    path('api/<int:resume_id>/analyze/', views.api_analyze_resume, name='api_analyze_resume'),
] 