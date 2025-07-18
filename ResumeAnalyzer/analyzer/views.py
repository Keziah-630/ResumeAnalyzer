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
    """Perform AI-powered resume analysis with ATS optimization"""
    
    # Extract text content
    content = f"{resume.skills} {resume.education} {resume.experience}".lower()
    
    # Define comprehensive skill categories and keywords
    technical_skills = [
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 'angular', 'vue',
        'node.js', 'django', 'flask', 'spring', 'docker', 'kubernetes', 'aws', 'azure',
        'git', 'github', 'jenkins', 'jira', 'agile', 'scrum', 'machine learning', 'ai',
        'data analysis', 'statistics', 'excel', 'powerbi', 'tableau', 'mongodb', 'postgresql',
        'mysql', 'redis', 'elasticsearch', 'kafka', 'spark', 'hadoop', 'tensorflow', 'pytorch',
        'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'r', 'sas',
        'spss', 'stata', 'powerpoint', 'word', 'outlook', 'teams', 'slack', 'zoom', 'trello',
        'asana', 'confluence', 'bitbucket', 'gitlab', 'vscode', 'intellij', 'eclipse',
        'android', 'ios', 'swift', 'kotlin', 'flutter', 'react native', 'xamarin'
    ]
    
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
        'time management', 'project management', 'customer service', 'sales', 'marketing',
        'research', 'analysis', 'planning', 'organization', 'creativity', 'adaptability',
        'collaboration', 'negotiation', 'presentation', 'mentoring', 'coaching', 'training',
        'strategic thinking', 'decision making', 'conflict resolution', 'emotional intelligence',
        'interpersonal skills', 'public speaking', 'writing', 'editing', 'proofreading'
    ]
    
    # ATS Optimization Keywords
    ats_keywords = [
        'results-driven', 'goal-oriented', 'detail-oriented', 'self-motivated', 'proactive',
        'innovative', 'strategic', 'analytical', 'methodical', 'systematic', 'efficient',
        'productive', 'reliable', 'dependable', 'flexible', 'adaptable', 'versatile',
        'multitasking', 'prioritization', 'deadline-oriented', 'quality-focused',
        'customer-focused', 'team-oriented', 'collaborative', 'cross-functional'
    ]
    
    # Extract skills
    extracted_skills = []
    skill_details = []
    ats_score = 0
    
    # Check for technical skills
    for skill in technical_skills:
        if skill in content:
            category = 'technical'
            relevance = 90 if skill in resume.skills.lower() else 70
            demand = 'high' if skill in ['python', 'javascript', 'react', 'aws', 'docker'] else 'medium'
            
            extracted_skills.append(skill)
            skill_details.append({
                'name': skill.title(),
                'relevance': relevance,
                'demand': demand,
                'category': category
            })
    
    # Check for soft skills
    for skill in soft_skills:
        if skill in content:
            category = 'soft'
            relevance = 85 if skill in resume.skills.lower() else 65
            demand = 'high' if skill in ['leadership', 'communication', 'problem solving'] else 'medium'
            
            extracted_skills.append(skill)
            skill_details.append({
                'name': skill.title(),
                'relevance': relevance,
                'demand': demand,
                'category': category
            })
    
    # ATS Optimization Analysis
    ats_found = []
    for keyword in ats_keywords:
        if keyword in content:
            ats_found.append(keyword)
            ats_score += 2
    
    # Calculate comprehensive scores
    skills_score = min(100, len(extracted_skills) * 8 + 20)  # Base 20 + 8 per skill
    experience_score = min(100, len(resume.experience.split()) * 0.3 + 30)  # Base 30 + 0.3 per word
    education_score = 85 if any(degree in resume.education.lower() for degree in ['bachelor', 'master', 'phd', 'degree']) else 60
    
    # ATS Formatting Score
    formatting_score = 70  # Base score
    if resume.full_name and resume.email and resume.phone:
        formatting_score += 10  # Contact info present
    if len(resume.skills.split(',')) >= 5:
        formatting_score += 10  # Good number of skills
    if len(resume.experience) > 100:
        formatting_score += 10  # Detailed experience
    
    # Add ATS score to formatting
    formatting_score = min(100, formatting_score + ats_score)
    
    overall_score = (skills_score + experience_score + education_score + formatting_score) / 4
    
    # Generate comprehensive insights
    insights = []
    
    # Skills analysis
    if skills_score < 70:
        insights.append({
            'type': 'skill_gap',
            'title': 'Skill Development Opportunity',
            'description': f'You have {len(extracted_skills)} skills identified. Consider adding more technical skills to improve your marketability.',
            'priority': 'high',
            'action_items': ['Learn Python programming', 'Get AWS certification', 'Practice data analysis', 'Add cloud computing skills']
        })
    else:
        insights.append({
            'type': 'strength',
            'title': 'Strong Skill Set',
            'description': f'Excellent! You have {len(extracted_skills)} skills identified, making you competitive in the job market.',
            'priority': 'low',
            'action_items': ['Continue learning new technologies', 'Stay updated with industry trends', 'Consider advanced certifications']
        })
    
    # Experience analysis
    if experience_score < 60:
        insights.append({
            'type': 'improvement',
            'title': 'Experience Enhancement',
            'description': 'Add more detailed descriptions of your work experience and achievements.',
            'priority': 'medium',
            'action_items': ['Quantify achievements with metrics', 'Add project descriptions', 'Include leadership roles', 'Use action verbs']
        })
    
    # ATS optimization insights
    if ats_score < 20:
        insights.append({
            'type': 'ats_optimization',
            'title': 'ATS Optimization Needed',
            'description': 'Your resume could benefit from more ATS-friendly keywords and formatting.',
            'priority': 'high',
            'action_items': ['Add more action verbs', 'Include industry-specific keywords', 'Use standard section headings', 'Avoid graphics and tables']
        })
    else:
        insights.append({
            'type': 'ats_optimization',
            'title': 'Good ATS Optimization',
            'description': f'Great! Your resume includes {len(ats_found)} ATS-friendly keywords.',
            'priority': 'low',
            'action_items': ['Maintain current optimization', 'Update keywords for specific job applications', 'Keep formatting clean and simple']
        })
    
    # Career path suggestions
    if any(skill in extracted_skills for skill in ['python', 'javascript', 'react', 'django']):
        insights.append({
            'type': 'career_path',
            'title': 'Software Development Career',
            'description': 'Based on your technical skills, you\'re well-positioned for software development roles.',
            'priority': 'medium',
            'action_items': ['Apply for software developer positions', 'Build portfolio projects', 'Contribute to open source', 'Network in tech communities']
        })
    elif any(skill in extracted_skills for skill in ['data analysis', 'statistics', 'excel', 'python']):
        insights.append({
            'type': 'career_path',
            'title': 'Data Analysis Career',
            'description': 'Your analytical skills make you suitable for data analysis and business intelligence roles.',
            'priority': 'medium',
            'action_items': ['Apply for data analyst positions', 'Learn SQL and visualization tools', 'Practice with real datasets', 'Get certified in data analysis']
        })
    
    # Generate skill gaps based on missing popular skills
    missing_skills = []
    popular_skills = ['python', 'javascript', 'sql', 'aws', 'docker', 'react', 'machine learning']
    for skill in popular_skills:
        if skill not in extracted_skills:
            missing_skills.append(skill.title())
    
    return {
        'overall_score': round(overall_score, 1),
        'skills_score': round(skills_score, 1),
        'experience_score': round(experience_score, 1),
        'education_score': round(education_score, 1),
        'formatting_score': round(formatting_score, 1),
        'extracted_skills': extracted_skills,
        'skill_gaps': missing_skills[:5],  # Top 5 missing skills
        'recommendations': [
            'Add more technical skills to increase marketability',
            'Quantify your achievements with specific metrics',
            'Include relevant certifications and training',
            'Optimize resume for ATS systems with keywords',
            'Use action verbs to describe your experience',
            'Keep formatting clean and professional'
        ],
        'industry_keywords': ['software development', 'data analysis', 'project management', 'agile methodology', 'cloud computing'],
        'skill_details': skill_details,
        'insights': insights,
        'ats_keywords_found': ats_found,
        'ats_score': ats_score
    }

@login_required
def api_analyze_resume(request, resume_id):
    """API endpoint for resume analysis"""
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        analysis_result = perform_resume_analysis(resume)
        return JsonResponse(analysis_result)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
