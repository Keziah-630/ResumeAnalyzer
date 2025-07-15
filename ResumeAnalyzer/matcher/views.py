from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from resumes.models import Resume
from jobs.models import Job, JobApplication
from .models import JobMatch, MatchPreference, MatchHistory
import json

@login_required
def job_matches(request):
    """Show job matches for the user"""
    user_resumes = Resume.objects.filter(user=request.user)
    
    if not user_resumes.exists():
        messages.warning(request, 'Please upload a resume first to see job matches.')
        return redirect('upload_resume')
    
    # Get user's preferences
    preferences, created = MatchPreference.objects.get_or_create(user=request.user)
    
    # Get or create matches
    matches = JobMatch.objects.filter(user=request.user, resume__in=user_resumes)
    
    if not matches.exists():
        # Generate matches for all user resumes
        for resume in user_resumes:
            generate_job_matches(request.user, resume)
        matches = JobMatch.objects.filter(user=request.user, resume__in=user_resumes)
    
    # Filter by preferences
    if preferences.match_threshold:
        matches = matches.filter(match_score__gte=preferences.match_threshold)
    
    # Pagination
    paginator = Paginator(matches, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'matches': page_obj,
        'preferences': preferences,
        'total_matches': matches.count(),
    }
    return render(request, 'matcher/job_matches.html', context)

@login_required
def match_detail(request, match_id):
    """Show detailed view of a job match"""
    match = get_object_or_404(JobMatch, id=match_id, user=request.user)
    
    # Mark as viewed
    if not match.is_viewed:
        match.is_viewed = True
        match.save()
        MatchHistory.objects.create(user=request.user, job_match=match, action='viewed')
    
    context = {
        'match': match,
        'job': match.job,
        'resume': match.resume,
    }
    return render(request, 'matcher/match_detail.html', context)

@login_required
def toggle_favorite(request, match_id):
    """Toggle favorite status of a job match"""
    match = get_object_or_404(JobMatch, id=match_id, user=request.user)
    match.is_favorite = not match.is_favorite
    match.save()
    
    action = 'favorited' if match.is_favorite else 'unfavorited'
    MatchHistory.objects.create(user=request.user, job_match=match, action='favorited' if match.is_favorite else 'dismissed')
    
    messages.success(request, f'Job {action} successfully!')
    return redirect('match_detail', match_id=match_id)

@login_required
def apply_from_match(request, match_id):
    """Apply to job from match view"""
    match = get_object_or_404(JobMatch, id=match_id, user=request.user)
    
    # Check if already applied
    if JobApplication.objects.filter(user=request.user, job=match.job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('match_detail', match_id=match_id)
    
    # Create application
    application = JobApplication.objects.create(
        user=request.user,
        job=match.job,
        resume=match.resume,
        match_score=match.match_score
    )
    
    # Update match status
    match.is_applied = True
    match.save()
    MatchHistory.objects.create(user=request.user, job_match=match, action='applied')
    
    messages.success(request, 'Application submitted successfully!')
    return redirect('match_detail', match_id=match_id)

@login_required
def match_preferences(request):
    """Manage job matching preferences"""
    preferences, created = MatchPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update preferences
        preferences.preferred_locations = request.POST.getlist('preferred_locations')
        preferences.preferred_job_types = request.POST.getlist('preferred_job_types')
        preferences.preferred_experience_levels = request.POST.getlist('preferred_experience_levels')
        preferences.required_skills = request.POST.getlist('required_skills')
        preferences.preferred_industries = request.POST.getlist('preferred_industries')
        preferences.email_notifications = 'email_notifications' in request.POST
        preferences.match_threshold = float(request.POST.get('match_threshold', 70))
        
        # Salary range
        salary_min = request.POST.get('salary_min')
        salary_max = request.POST.get('salary_max')
        preferences.salary_min = float(salary_min) if salary_min else None
        preferences.salary_max = float(salary_max) if salary_max else None
        
        preferences.save()
        
        # Regenerate matches with new preferences
        user_resumes = Resume.objects.filter(user=request.user)
        for resume in user_resumes:
            generate_job_matches(request.user, resume)
        
        messages.success(request, 'Preferences updated and matches regenerated!')
        return redirect('job_matches')
    
    context = {
        'preferences': preferences,
        'job_types': Job.JOB_TYPE_CHOICES,
        'experience_levels': Job.EXPERIENCE_LEVEL_CHOICES,
    }
    return render(request, 'matcher/preferences.html', context)

@login_required
def match_history(request):
    """Show user's match interaction history"""
    history = MatchHistory.objects.filter(user=request.user).select_related('job_match__job')
    
    # Pagination
    paginator = Paginator(history, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'history': page_obj,
    }
    return render(request, 'matcher/history.html', context)

def generate_job_matches(user, resume):
    """Generate job matches for a user's resume"""
    # Get all active jobs
    jobs = Job.objects.filter(is_active=True)
    
    for job in jobs:
        # Calculate match score
        match_score, skills_match, experience_match, location_match = calculate_match_score(resume, job)
        
        # Get matching and missing skills
        matching_skills, missing_skills = get_skill_matches(resume, job)
        
        # Get match reasons
        match_reasons = get_match_reasons(resume, job, match_score)
        
        # Create or update match
        match, created = JobMatch.objects.get_or_create(
            user=user,
            resume=resume,
            job=job,
            defaults={
                'match_score': match_score,
                'skills_match': skills_match,
                'experience_match': experience_match,
                'location_match': location_match,
                'matching_skills': matching_skills,
                'missing_skills': missing_skills,
                'match_reasons': match_reasons,
            }
        )
        
        if not created:
            # Update existing match
            match.match_score = match_score
            match.skills_match = skills_match
            match.experience_match = experience_match
            match.location_match = location_match
            match.matching_skills = matching_skills
            match.missing_skills = missing_skills
            match.match_reasons = match_reasons
            match.save()

def calculate_match_score(resume, job):
    """Calculate match score between resume and job"""
    # Skills match (40% weight)
    resume_skills = set(resume.skills.lower().split(','))
    job_skills = set(job.skills_required.lower().split(','))
    
    if job_skills:
        skills_match = len(resume_skills & job_skills) / len(job_skills) * 100
    else:
        skills_match = 0
    
    # Experience match (30% weight)
    experience_match = 70  # Placeholder - could be more sophisticated
    
    # Location match (20% weight)
    location_match = 80  # Placeholder - could check actual location matching
    
    # Other factors (10% weight)
    other_match = 75  # Placeholder
    
    # Calculate overall score
    overall_score = (skills_match * 0.4 + experience_match * 0.3 + location_match * 0.2 + other_match * 0.1)
    
    return round(overall_score, 1), round(skills_match, 1), round(experience_match, 1), round(location_match, 1)

def get_skill_matches(resume, job):
    """Get matching and missing skills"""
    resume_skills = set(resume.skills.lower().split(','))
    job_skills = set(job.skills_required.lower().split(','))
    
    matching_skills = list(resume_skills & job_skills)
    missing_skills = list(job_skills - resume_skills)
    
    return matching_skills, missing_skills

def get_match_reasons(resume, job, match_score):
    """Get reasons for the match score"""
    reasons = []
    
    if match_score >= 80:
        reasons.append("Excellent skills match")
        reasons.append("Strong experience alignment")
    elif match_score >= 60:
        reasons.append("Good skills overlap")
        reasons.append("Relevant experience")
    else:
        reasons.append("Some skills match")
        reasons.append("Consider skill development")
    
    return reasons
