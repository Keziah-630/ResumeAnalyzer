from django.core.management.base import BaseCommand
from jobs.models import Job
import random

class Command(BaseCommand):
    help = 'Create demo jobs with random company names and skills.'

    def handle(self, *args, **options):
        titles = [
            'Software Engineer', 'Data Analyst', 'Web Developer', 'AI Researcher',
            'Network Administrator', 'Cloud Architect', 'QA Tester', 'DevOps Engineer',
            'Mobile App Developer', 'UI/UX Designer', 'Product Manager', 'Business Analyst'
        ]
        companies = [
            'Unknown Corp', 'Mystery Solutions', 'TechNova', 'FutureWorks', 'SkyNet',
            'QuantumLeap', 'InnoSoft', 'NextGen', 'AlphaOmega', 'BetaBytes', 'DeltaForce', 'ZetaTech'
        ]
        locations = ['Remote', 'Hyderabad', 'Bangalore', 'Chennai', 'Pune', 'Delhi', 'Mumbai']
        job_types = ['full-time', 'part-time', 'contract', 'internship', 'freelance']
        experience_levels = ['entry', 'junior', 'mid', 'senior', 'lead']
        skills = [
            'Python', 'Django', 'JavaScript', 'React', 'SQL', 'AWS', 'Docker', 'Kubernetes',
            'Machine Learning', 'Data Science', 'HTML', 'CSS', 'REST API', 'Linux', 'Agile', 'Scrum'
        ]
        for i in range(10):
            title = random.choice(titles)
            company = random.choice(companies)
            location = random.choice(locations)
            job_type = random.choice(job_types)
            experience_level = random.choice(experience_levels)
            salary_min = random.randint(300000, 800000)
            salary_max = salary_min + random.randint(100000, 500000)
            description = f"Exciting opportunity for a {title} at {company}. Join our team!"
            requirements = f"Experience with {random.choice(skills)}, {random.choice(skills)}, and {random.choice(skills)}."
            skills_required = ', '.join(random.sample(skills, 5))
            benefits = 'Health insurance, Paid time off, Flexible hours'
            contact_email = f"hr@{company.lower().replace(' ', '')}.com"
            application_url = ''
            is_active = True
            job = Job.objects.create(
                title=title,
                company=company,
                location=location,
                job_type=job_type,
                experience_level=experience_level,
                salary_min=salary_min,
                salary_max=salary_max,
                description=description,
                requirements=requirements,
                skills_required=skills_required,
                benefits=benefits,
                contact_email=contact_email,
                application_url=application_url,
                is_active=is_active
            )
            self.stdout.write(self.style.SUCCESS(f'Created job: {title} at {company}'))
        self.stdout.write(self.style.SUCCESS('Demo jobs created successfully!')) 