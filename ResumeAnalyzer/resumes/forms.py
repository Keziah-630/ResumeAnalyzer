from django import forms
from .models import Resume
import re

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'full_name', 'email', 'phone', 'github', 'linkedin',
            'skills', 'education', 'experience', 'resume_file'
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 2}),
            'education': forms.Textarea(attrs={'rows': 2}),
            'experience': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\+?\d{10,15}$', phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean_resume_file(self):
        file = self.cleaned_data.get('resume_file')
        if file:
            if not file.name.endswith(('.pdf', '.doc', '.docx')):
                raise forms.ValidationError("Only PDF, DOC, and DOCX files are allowed.")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB.")
        return file