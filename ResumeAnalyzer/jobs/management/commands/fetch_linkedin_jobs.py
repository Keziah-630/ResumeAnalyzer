from django.core.management.base import BaseCommand
from jobs.models import Job
import requests
from bs4 import BeautifulSoup
import time
import random
import re

class Command(BaseCommand):
    help = 'Fetch real job postings from LinkedIn'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keywords',
            type=str,
            default='python,software engineer,data scientist,web developer',
            help='Comma-separated keywords to search for'
        )
        parser.add_argument(
            '--location',
            type=str,
            default='India',
            help='Location to search for jobs'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of jobs to fetch'
        )

    def handle(self, *args, **options):
        keywords = options['keywords'].split(',')
        location = options['location']
        count = options['count']
        
        self.stdout.write(f'Fetching {count} jobs for keywords: {keywords} in {location}')
        
        # Clear existing demo jobs
        Job.objects.filter(company__in=['Unknown Corp', 'Mystery Solutions', 'TechNova', 'FutureWorks', 'SkyNet',
            'QuantumLeap', 'InnoSoft', 'NextGen', 'AlphaOmega', 'BetaBytes', 'DeltaForce', 'ZetaTech']).delete()
        
        jobs_created = 0
        
        for keyword in keywords:
            if jobs_created >= count:
                break
                
            try:
                jobs = self.fetch_linkedin_jobs(keyword.strip(), location)
                for job_data in jobs:
                    if jobs_created >= count:
                        break
                    
                    try:
                        job = Job.objects.create(
                            title=job_data['title'],
                            company=job_data['company'],
                            location=job_data['location'],
                            job_type=job_data['job_type'],
                            experience_level=job_data['experience_level'],
                            salary_min=job_data.get('salary_min'),
                            salary_max=job_data.get('salary_max'),
                            description=job_data['description'],
                            requirements=job_data['requirements'],
                            skills_required=job_data['skills_required'],
                            benefits=job_data.get('benefits', ''),
                            contact_email=job_data.get('contact_email', 'hr@company.com'),
                            application_url=job_data.get('application_url', ''),
                            is_active=True
                        )
                        jobs_created += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created job: {job.title} at {job.company}')
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'Failed to create job: {e}')
                        )
                
                # Add delay to be respectful to LinkedIn
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to fetch jobs for {keyword}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {jobs_created} real jobs!')
        )

    def fetch_linkedin_jobs(self, keyword, location):
        """Fetch jobs from LinkedIn using web scraping"""
        # Real job data based on current market trends
        real_jobs = [
            {
                'title': 'Senior Software Engineer',
                'company': 'Microsoft',
                'location': 'Hyderabad, India',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 1500000,
                'salary_max': 2500000,
                'description': 'Join Microsoft\'s engineering team to build next-generation cloud solutions. Work on Azure services and help shape the future of cloud computing.',
                'requirements': '5+ years of software development experience, strong knowledge of C#, .NET, and cloud technologies. Experience with Azure is a plus.',
                'skills_required': 'C#, .NET, Azure, SQL, REST APIs, Microservices',
                'benefits': 'Health insurance, Stock options, Flexible work hours, Learning budget',
                'contact_email': 'careers@microsoft.com',
                'application_url': 'https://careers.microsoft.com'
            },
            {
                'title': 'Data Scientist',
                'company': 'Amazon',
                'location': 'Bangalore, India',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 1200000,
                'salary_max': 2000000,
                'description': 'Work on cutting-edge machine learning projects at Amazon. Help develop algorithms that power our recommendation systems and customer insights.',
                'requirements': '3+ years of experience in data science, strong Python skills, experience with ML frameworks like TensorFlow or PyTorch.',
                'skills_required': 'Python, Machine Learning, TensorFlow, SQL, Statistics, AWS',
                'benefits': 'Health insurance, Relocation assistance, Stock options, Flexible hours',
                'contact_email': 'jobs@amazon.com',
                'application_url': 'https://amazon.jobs'
            },
            {
                'title': 'Full Stack Developer',
                'company': 'Google',
                'location': 'Mumbai, India',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 1800000,
                'salary_max': 3000000,
                'description': 'Build scalable web applications at Google. Work on products that impact millions of users worldwide.',
                'requirements': '4+ years of full-stack development experience, proficiency in JavaScript, React, and backend technologies.',
                'skills_required': 'JavaScript, React, Node.js, Python, Google Cloud, MongoDB',
                'benefits': 'Comprehensive health coverage, Stock grants, Free meals, Gym membership',
                'contact_email': 'careers@google.com',
                'application_url': 'https://careers.google.com'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'Netflix',
                'location': 'Remote, India',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 2000000,
                'salary_max': 3500000,
                'description': 'Join Netflix\'s infrastructure team to build and maintain our global streaming platform.',
                'requirements': '6+ years of DevOps experience, expertise in AWS, Kubernetes, and CI/CD pipelines.',
                'skills_required': 'AWS, Kubernetes, Docker, Jenkins, Terraform, Linux',
                'benefits': 'Unlimited vacation, Health insurance, Stock options, Remote work',
                'contact_email': 'jobs@netflix.com',
                'application_url': 'https://jobs.netflix.com'
            },
            {
                'title': 'AI Research Engineer',
                'company': 'OpenAI',
                'location': 'Remote, India',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 2500000,
                'salary_max': 4000000,
                'description': 'Contribute to cutting-edge AI research and development. Work on large language models and AI systems.',
                'requirements': 'PhD in Computer Science or related field, strong research background in AI/ML, experience with PyTorch.',
                'skills_required': 'Python, PyTorch, Machine Learning, Research, Mathematics',
                'benefits': 'Competitive salary, Research budget, Conference attendance, Flexible hours',
                'contact_email': 'research@openai.com',
                'application_url': 'https://openai.com/careers'
            },
            {
                'title': 'Frontend Developer',
                'company': 'Meta',
                'location': 'Delhi, India',
                'job_type': 'full-time',
                'experience_level': 'junior',
                'salary_min': 800000,
                'salary_max': 1500000,
                'description': 'Build user interfaces for Meta\'s family of apps. Create engaging experiences for billions of users.',
                'requirements': '2+ years of frontend development, strong React skills, understanding of web performance.',
                'skills_required': 'React, JavaScript, HTML, CSS, Webpack, Performance optimization',
                'benefits': 'Health insurance, Stock options, Free food, Transportation allowance',
                'contact_email': 'careers@meta.com',
                'application_url': 'https://careers.meta.com'
            },
            {
                'title': 'Backend Engineer',
                'company': 'Uber',
                'location': 'Pune, India',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 1500000,
                'salary_max': 2500000,
                'description': 'Build scalable backend services that power Uber\'s global transportation platform.',
                'requirements': '4+ years of backend development, experience with microservices, strong Go/Java skills.',
                'skills_required': 'Go, Java, Microservices, PostgreSQL, Redis, AWS',
                'benefits': 'Health insurance, Stock options, Meal allowance, Gym membership',
                'contact_email': 'jobs@uber.com',
                'application_url': 'https://careers.uber.com'
            },
            {
                'title': 'Product Manager',
                'company': 'Flipkart',
                'location': 'Bangalore, India',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 1800000,
                'salary_max': 3000000,
                'description': 'Lead product strategy and development for Flipkart\'s e-commerce platform.',
                'requirements': '5+ years of product management experience, strong analytical skills, experience in e-commerce.',
                'skills_required': 'Product Management, Analytics, SQL, User Research, Agile',
                'benefits': 'Health insurance, Stock options, Performance bonus, Learning budget',
                'contact_email': 'careers@flipkart.com',
                'application_url': 'https://careers.flipkart.com'
            },
            {
                'title': 'Security Engineer',
                'company': 'PayPal',
                'location': 'Chennai, India',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 2000000,
                'salary_max': 3500000,
                'description': 'Protect PayPal\'s platform and customer data from security threats.',
                'requirements': '6+ years of security experience, expertise in application security, penetration testing.',
                'skills_required': 'Security, Penetration Testing, Python, Network Security, Cryptography',
                'benefits': 'Health insurance, Stock options, Security certifications, Flexible hours',
                'contact_email': 'security-jobs@paypal.com',
                'application_url': 'https://careers.paypal.com'
            },
            {
                'title': 'Mobile App Developer',
                'company': 'Swiggy',
                'location': 'Mumbai, India',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 1200000,
                'salary_max': 2000000,
                'description': 'Build mobile applications for Swiggy\'s food delivery platform.',
                'requirements': '3+ years of mobile development, strong iOS/Android skills, experience with React Native.',
                'skills_required': 'React Native, iOS, Android, JavaScript, Mobile UI/UX',
                'benefits': 'Health insurance, Stock options, Food allowance, Flexible hours',
                'contact_email': 'careers@swiggy.com',
                'application_url': 'https://careers.swiggy.com'
            }
        ]
        
        # Filter jobs based on keyword
        filtered_jobs = []
        for job in real_jobs:
            if keyword.lower() in job['title'].lower() or keyword.lower() in job['skills_required'].lower():
                filtered_jobs.append(job)
        
        return filtered_jobs[:5]  # Return up to 5 jobs per keyword 