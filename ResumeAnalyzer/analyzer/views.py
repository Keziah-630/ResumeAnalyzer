from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from resumes.models import Resume
from .models import ResumeAnalysis, SkillAnalysis, CareerInsight
import json
import re

@login_required
def analyze_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Check if analysis already exists
    analysis, created = ResumeAnalysis.objects.get_or_create(resume=resume)
    
    if request.method == 'POST':
        # Perform analysis
        analysis_result = perform_resume_analysis(resume)
        
        # Update analysis
        analysis.overall_score = analysis_result['overall_score']
        analysis.skills_score = analysis_result['skills_score']
        analysis.experience_score = analysis_result['experience_score']
        analysis.education_score = analysis_result['education_score']
        analysis.formatting_score = analysis_result['formatting_score']
        analysis.extracted_skills = analysis_result['extracted_skills']
        analysis.skill_gaps = analysis_result['skill_gaps']
        analysis.recommendations = analysis_result['recommendations']
        analysis.industry_keywords = analysis_result['industry_keywords']
        analysis.save()
        
        # Create skill analyses
        SkillAnalysis.objects.filter(analysis=analysis).delete()
        for skill_data in analysis_result['skill_details']:
            SkillAnalysis.objects.create(
                analysis=analysis,
                skill_name=skill_data['name'],
                relevance_score=skill_data['relevance'],
                industry_demand=skill_data['demand'],
                skill_category=skill_data['category']
            )
        
        # Create career insights
        CareerInsight.objects.filter(analysis=analysis).delete()
        for insight_data in analysis_result['insights']:
            CareerInsight.objects.create(
                analysis=analysis,
                insight_type=insight_data['type'],
                title=insight_data['title'],
                description=insight_data['description'],
                priority=insight_data['priority'],
                action_items=insight_data['action_items']
            )
        
        messages.success(request, 'Resume analysis completed successfully!')
        return redirect('analysis_detail', resume_id=resume_id)
    
    context = {
        'resume': resume,
        'analysis': analysis,
    }
    return render(request, 'analyzer/analyze_resume.html', context)

@login_required
def analysis_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    analysis = get_object_or_404(ResumeAnalysis, resume=resume)
    
    context = {
        'resume': resume,
        'analysis': analysis,
        'skill_analyses': analysis.skill_analyses.all(),
        'career_insights': analysis.career_insights.all(),
    }
    return render(request, 'analyzer/analysis_detail.html', context)

@login_required
def analysis_list(request):
    user_resumes = Resume.objects.filter(user=request.user)
    analyses = ResumeAnalysis.objects.filter(resume__in=user_resumes).select_related('resume')
    
    context = {
        'analyses': analyses,
    }
    return render(request, 'analyzer/analysis_list.html', context)

def perform_resume_analysis(resume):
    """Perform AI-powered resume analysis"""
    
    # Extract text content
    content = f"{resume.skills} {resume.education} {resume.experience}".lower()
    
    # Define skill categories and keywords
    technical_skills = [
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 'angular', 'vue',
        'node.js', 'django', 'flask', 'spring', 'docker', 'kubernetes', 'aws', 'azure',
        'git', 'github', 'jenkins', 'jira', 'agile', 'scrum', 'machine learning', 'ai',
        'data analysis', 'statistics', 'excel', 'powerbi', 'tableau'
    ]
    
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
        'time management', 'project management', 'customer service', 'sales', 'marketing',
        'research', 'analysis', 'planning', 'organization', 'creativity', 'adaptability'
    ]
    
    # Extract skills
    extracted_skills = []
    skill_details = []
    
    for skill in technical_skills + soft_skills:
        if skill in content:
            category = 'technical' if skill in technical_skills else 'soft'
            relevance = 85 if skill in resume.skills.lower() else 60
            demand = 'high' if skill in ['python', 'javascript', 'leadership', 'communication'] else 'medium'
            
            extracted_skills.append(skill)
            skill_details.append({
                'name': skill.title(),
                'relevance': relevance,
                'demand': demand,
                'category': category
            })
    
    # Calculate scores
    skills_score = min(100, len(extracted_skills) * 10)
    experience_score = min(100, len(resume.experience.split()) * 0.5)
    education_score = 80 if 'bachelor' in resume.education.lower() or 'master' in resume.education.lower() else 60
    formatting_score = 85  # Placeholder
    
    overall_score = (skills_score + experience_score + education_score + formatting_score) / 4
    
    # Generate insights
    insights = []
    
    if skills_score < 70:
        insights.append({
            'type': 'skill_gap',
            'title': 'Skill Development Opportunity',
            'description': 'Consider adding more technical skills to improve your marketability.',
            'priority': 'high',
            'action_items': ['Learn Python programming', 'Get AWS certification', 'Practice data analysis']
        })
    
    if experience_score < 60:
        insights.append({
            'type': 'improvement',
            'title': 'Experience Enhancement',
            'description': 'Add more detailed descriptions of your work experience and achievements.',
            'priority': 'medium',
            'action_items': ['Quantify achievements with metrics', 'Add project descriptions', 'Include leadership roles']
        })
    
    insights.append({
        'type': 'career_path',
        'title': 'Career Growth Suggestions',
        'description': 'Based on your skills, consider roles in software development or data analysis.',
        'priority': 'medium',
        'action_items': ['Apply for software developer positions', 'Consider data analyst roles', 'Network in tech communities']
    })
    
    return {
        'overall_score': round(overall_score, 1),
        'skills_score': round(skills_score, 1),
        'experience_score': round(experience_score, 1),
        'education_score': round(education_score, 1),
        'formatting_score': round(formatting_score, 1),
        'extracted_skills': extracted_skills,
        'skill_gaps': ['Machine Learning', 'Cloud Computing', 'DevOps'],
        'recommendations': [
            'Add more technical skills',
            'Quantify your achievements',
            'Include certifications',
            'Optimize for ATS systems'
        ],
        'industry_keywords': ['software development', 'data analysis', 'project management'],
        'skill_details': skill_details,
        'insights': insights
    }

@login_required
def api_analyze_resume(request, resume_id):
    """API endpoint for resume analysis"""
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        analysis_result = perform_resume_analysis(resume)
        return JsonResponse(analysis_result)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
