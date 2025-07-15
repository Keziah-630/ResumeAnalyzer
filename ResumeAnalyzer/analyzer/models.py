from django.db import models
from django.contrib.auth.models import User
from resumes.models import Resume

class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skills_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    experience_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    education_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    formatting_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Analysis details
    extracted_skills = models.JSONField(default=list, blank=True)
    skill_gaps = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    industry_keywords = models.JSONField(default=list, blank=True)
    
    # Analysis metadata
    analysis_date = models.DateTimeField(auto_now_add=True)
    analysis_version = models.CharField(max_length=20, default='1.0')
    
    def __str__(self):
        return f"Analysis for {self.resume.full_name}"
    
    @property
    def score_color(self):
        if self.overall_score:
            if self.overall_score >= 80:
                return 'success'
            elif self.overall_score >= 60:
                return 'warning'
            else:
                return 'danger'
        return 'secondary'

class SkillAnalysis(models.Model):
    analysis = models.ForeignKey(ResumeAnalysis, on_delete=models.CASCADE, related_name='skill_analyses')
    skill_name = models.CharField(max_length=100)
    relevance_score = models.DecimalField(max_digits=5, decimal_places=2)
    industry_demand = models.CharField(max_length=20, choices=[
        ('high', 'High Demand'),
        ('medium', 'Medium Demand'),
        ('low', 'Low Demand'),
    ])
    skill_category = models.CharField(max_length=50, choices=[
        ('technical', 'Technical Skills'),
        ('soft', 'Soft Skills'),
        ('language', 'Programming Languages'),
        ('tools', 'Tools & Technologies'),
        ('certification', 'Certifications'),
    ])
    
    def __str__(self):
        return f"{self.skill_name} - {self.relevance_score}"

class CareerInsight(models.Model):
    analysis = models.ForeignKey(ResumeAnalysis, on_delete=models.CASCADE, related_name='career_insights')
    insight_type = models.CharField(max_length=50, choices=[
        ('skill_gap', 'Skill Gap'),
        ('career_path', 'Career Path'),
        ('market_trend', 'Market Trend'),
        ('improvement', 'Improvement Suggestion'),
    ])
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ])
    action_items = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.insight_type}: {self.title}"
