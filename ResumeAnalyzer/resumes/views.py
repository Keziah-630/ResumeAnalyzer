from django.shortcuts import render, redirect, get_object_or_404
from .forms import ResumeForm
from .models import Resume
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from analyzer.models import ResumeAnalysis
from matcher.models import JobMatch

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            
            # Generate job matches for the new resume
            from matcher.views import generate_job_matches
            generate_job_matches(request.user, resume)
            
            messages.success(request, "Resume uploaded successfully! Job matches have been generated.")
            return redirect('resume_list')
        else:
            messages.error(request, "Please correct the highlighted errors.")
    else:
        form = ResumeForm()
    return render(request, 'resumes/upload_resume.html', {'form': form})

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    
    # Get analysis status for each resume
    for resume in resumes:
        resume.has_analysis = ResumeAnalysis.objects.filter(resume=resume).exists()
        resume.match_count = JobMatch.objects.filter(resume=resume, user=request.user).count()
    
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Get analysis if exists
    try:
        analysis = ResumeAnalysis.objects.get(resume=resume)
    except ResumeAnalysis.DoesNotExist:
        analysis = None
    
    # Get job matches
    matches = JobMatch.objects.filter(resume=resume, user=request.user).order_by('-match_score')[:5]
    
    context = {
        'resume': resume,
        'analysis': analysis,
        'matches': matches,
    }
    return render(request, 'resumes/resume_detail.html', context)

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully!')
        return redirect('resume_list')
    
    return render(request, 'resumes/delete_resume.html', {'resume': resume})