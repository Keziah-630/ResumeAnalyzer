from django import forms
from .models import Job, JobApplication

CITIES = [
    ('', 'All Locations'),
    ('Mumbai', 'Mumbai'),
    ('Delhi', 'Delhi'),
    ('Bangalore', 'Bangalore'),
    ('Hyderabad', 'Hyderabad'),
    ('Chennai', 'Chennai'),
    ('Pune', 'Pune'),
    ('Kolkata', 'Kolkata'),
    ('Ahmedabad', 'Ahmedabad'),
    ('Other', 'Other / Custom'),
]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company', 'location', 'job_type', 'experience_level',
            'salary_min', 'salary_max', 'description', 'requirements',
            'skills_required', 'benefits', 'contact_email', 'application_url'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Title'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location (City, State)'
            }),
            'job_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'experience_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'salary_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum Salary'
            }),
            'salary_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum Salary'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Job Description'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Job Requirements'
            }),
            'skills_required': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Required Skills (comma-separated)'
            }),
            'benefits': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Benefits and Perks'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Email'
            }),
            'application_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Application URL (optional)'
            }),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']
        widgets = {
            'resume': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your cover letter here...'
            }),
        }

TRENDING_JOB_TITLES = [
    'Data Scientist', 'Data Analyst', 'Machine Learning Engineer', 'Software Engineer',
    'Backend Developer', 'Frontend Developer', 'Full Stack Developer', 'Cloud Engineer',
    'DevOps Engineer', 'Cybersecurity Analyst', 'Product Manager', 'UI/UX Designer',
    'Business Analyst', 'Digital Marketing Specialist', 'AI Researcher', 'Blockchain Developer',
    'Mobile App Developer', 'QA Engineer', 'IT Support Specialist', 'Project Manager',
    'Network Engineer', 'Systems Administrator', 'Database Administrator', 'Content Writer',
    'Graphic Designer', 'Sales Manager', 'Marketing Manager', 'Financial Analyst', 'HR Specialist',
    'Operations Manager', 'Other',
]

class JobSearchForm(forms.Form):
    job_title = forms.ChoiceField(
        required=False,
        choices=[('', 'All Titles')] + [(title, title) for title in TRENDING_JOB_TITLES],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'job-title-select',
        })
    )
    custom_job_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom job title',
            'id': 'custom-job-title-input',
            'style': 'display:none;',
        })
    )
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search jobs...'
        })
    )
    location = forms.ChoiceField(
        choices=CITIES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'location-select',
        })
    )
    custom_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your city',
            'id': 'custom-location-input',
            'style': 'display:none;',
        })
    )
    job_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Job.JOB_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    experience_level = forms.ChoiceField(
        choices=[('', 'All Levels')] + Job.EXPERIENCE_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No longer populating from DB, using hardcoded trending titles
        # job_titles = Job.objects.values_list('title', flat=True).distinct()
        # choices = [('', 'All Titles')] + [(title, title) for title in job_titles]
        # self.fields['job_title'].choices = choices 