from django.db import models
from django.contrib.auth.models import User
from resumes.models import Resume
from jobs.models import Job

class JobMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    match_score = models.DecimalField(max_digits=5, decimal_places=2)
    skills_match = models.DecimalField(max_digits=5, decimal_places=2)
    experience_match = models.DecimalField(max_digits=5, decimal_places=2)
    location_match = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Match details
    matching_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    match_reasons = models.JSONField(default=list, blank=True)
    
    # User interaction
    is_favorite = models.BooleanField(default=False)
    is_viewed = models.BooleanField(default=False)
    is_applied = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'resume', 'job']
        ordering = ['-match_score']
    
    def __str__(self):
        return f"{self.user.username} - {self.job.title} ({self.match_score}%)"
    
    @property
    def match_level(self):
        if self.match_score >= 90:
            return 'excellent'
        elif self.match_score >= 80:
            return 'very_good'
        elif self.match_score >= 70:
            return 'good'
        elif self.match_score >= 60:
            return 'fair'
        else:
            return 'poor'
    
    def get_match_level_display(self):
        """Get human-readable match level"""
        levels = {
            'excellent': 'Excellent Match',
            'very_good': 'Very Good Match',
            'good': 'Good Match',
            'fair': 'Fair Match',
            'poor': 'Poor Match'
        }
        return levels.get(self.match_level, 'Unknown')

class MatchPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preferred_locations = models.JSONField(default=list, blank=True)
    preferred_job_types = models.JSONField(default=list, blank=True)
    preferred_experience_levels = models.JSONField(default=list, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    required_skills = models.JSONField(default=list, blank=True)
    preferred_industries = models.JSONField(default=list, blank=True)
    
    # Notification settings
    email_notifications = models.BooleanField(default=True)
    match_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=70.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"

class MatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_match = models.ForeignKey(JobMatch, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=[
        ('viewed', 'Viewed'),
        ('favorited', 'Favorited'),
        ('applied', 'Applied'),
        ('dismissed', 'Dismissed'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} {self.action} {self.job_match.job.title}"
