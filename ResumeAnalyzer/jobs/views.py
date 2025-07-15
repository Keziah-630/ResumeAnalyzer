from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm, JobSearchForm
from resumes.models import Resume

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    
    # Search functionality
    search_form = JobSearchForm(request.GET)
    if search_form.is_valid():
        keyword = search_form.cleaned_data.get('keyword')
        location = search_form.cleaned_data.get('location')
        job_type = search_form.cleaned_data.get('job_type')
        experience_level = search_form.cleaned_data.get('experience_level')
        
        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(company__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(skills_required__icontains=keyword)
            )
        
        if location:
            jobs = jobs.filter(location__icontains=location)
        
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'search_form': search_form,
        'total_jobs': jobs.count(),
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    user_has_applied = False
    user_application = None
    
    if request.user.is_authenticated:
        user_has_applied = JobApplication.objects.filter(user=request.user, job=job).exists()
        if user_has_applied:
            user_application = JobApplication.objects.get(user=request.user, job=job)
    
    context = {
        'job': job,
        'user_has_applied': user_has_applied,
        'user_application': user_application,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if user already applied
    if JobApplication.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            
            # Calculate match score (simplified version)
            if application.resume:
                resume_skills = application.resume.skills.lower().split(',')
                job_skills = job.skills_required.lower().split(',')
                matching_skills = set(resume_skills) & set(job_skills)
                if job_skills:
                    match_percentage = (len(matching_skills) / len(job_skills)) * 100
                    application.match_score = min(match_percentage, 100)
            
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', job_id=job_id)
    else:
        form = JobApplicationForm()
        # Pre-populate with user's resumes
        form.fields['resume'].queryset = Resume.objects.filter(user=request.user)
    
    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'jobs/apply_job.html', context)

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(user=request.user).order_by('-applied_at')
    
    context = {
        'applications': applications,
    }
    return render(request, 'jobs/my_applications.html', context)

@login_required
def withdraw_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, user=request.user)
    job_id = application.job.id
    application.delete()
    messages.success(request, 'Application withdrawn successfully.')
    return redirect('job_detail', job_id=job_id)

# Admin views for job management
@login_required
def create_job(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create jobs.')
        return redirect('job_list')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job_list')
    else:
        form = JobForm()
    
    context = {
        'form': form,
        'title': 'Create New Job',
    }
    return render(request, 'jobs/job_form.html', context)

@login_required
def edit_job(request, job_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit jobs.')
        return redirect('job_list')
    
    job = get_object_or_404(Job, id=job_id)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', job_id=job_id)
    else:
        form = JobForm(instance=job)
    
    context = {
        'form': form,
        'job': job,
        'title': 'Edit Job',
    }
    return render(request, 'jobs/job_form.html', context)

@login_required
def delete_job(request, job_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete jobs.')
        return redirect('job_list')
    
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('job_list')
    
    context = {
        'job': job,
    }
    return render(request, 'jobs/delete_job.html', context)
