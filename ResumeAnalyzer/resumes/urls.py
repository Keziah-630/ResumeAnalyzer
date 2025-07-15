from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_list, name='resume_list'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),
]