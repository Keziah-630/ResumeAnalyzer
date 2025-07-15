from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    skills = models.TextField()
    education = models.TextField()
    experience = models.TextField()
    resume_file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.full_name} ({self.email})"
