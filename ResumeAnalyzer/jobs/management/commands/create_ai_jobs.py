from django.core.management.base import BaseCommand
from jobs.models import Job

class Command(BaseCommand):
    help = 'Create AI/Data Science specific jobs for demo purposes.'

    def handle(self, *args, **options):
        ai_jobs = [
            {
                'title': 'Machine Learning Engineer',
                'company': 'TechNova AI',
                'location': 'Hyderabad',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 800000,
                'salary_max': 1500000,
                'description': 'Join our AI team to build cutting-edge machine learning models and deploy them in production.',
                'requirements': 'Strong background in Python, TensorFlow, PyTorch, and ML algorithms. Experience with cloud platforms preferred.',
                'skills_required': 'Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, AWS, Docker, SQL',
                'benefits': 'Health insurance, Flexible hours, Learning budget, Stock options',
                'contact_email': 'hr@technovaai.com'
            },
            {
                'title': 'Data Scientist',
                'company': 'DataCorp Solutions',
                'location': 'Bangalore',
                'job_type': 'full-time',
                'experience_level': 'junior',
                'salary_min': 600000,
                'salary_max': 1000000,
                'description': 'Analyze large datasets and develop predictive models to drive business decisions.',
                'requirements': 'Experience with statistical analysis, data visualization, and machine learning algorithms.',
                'skills_required': 'Python, Pandas, NumPy, Scikit-learn, SQL, Data Analysis, Statistical Analysis',
                'benefits': 'Health insurance, Remote work options, Professional development',
                'contact_email': 'careers@datacorp.com'
            },
            {
                'title': 'AI Research Engineer',
                'company': 'FutureWorks',
                'location': 'Remote',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 1200000,
                'salary_max': 2000000,
                'description': 'Research and develop next-generation AI models for natural language processing and computer vision.',
                'requirements': 'PhD or MS in Computer Science with focus on AI/ML. Published research preferred.',
                'skills_required': 'Python, Deep Learning, Natural Language Processing, Computer Vision, PyTorch, Research',
                'benefits': 'Competitive salary, Research budget, Conference attendance, Flexible hours',
                'contact_email': 'research@futureworks.ai'
            },
            {
                'title': 'MLOps Engineer',
                'company': 'CloudTech Systems',
                'location': 'Chennai',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 900000,
                'salary_max': 1400000,
                'description': 'Build and maintain ML infrastructure for model deployment and monitoring.',
                'requirements': 'Experience with ML model deployment, containerization, and cloud platforms.',
                'skills_required': 'Python, Docker, Kubernetes, AWS, Machine Learning, CI/CD, Monitoring',
                'benefits': 'Health insurance, Learning opportunities, Performance bonuses',
                'contact_email': 'jobs@cloudtech.com'
            },
            {
                'title': 'Computer Vision Engineer',
                'company': 'VisionAI Labs',
                'location': 'Pune',
                'job_type': 'full-time',
                'experience_level': 'junior',
                'salary_min': 700000,
                'salary_max': 1100000,
                'description': 'Develop computer vision algorithms for image and video processing applications.',
                'requirements': 'Strong background in computer vision, deep learning, and image processing.',
                'skills_required': 'Python, Computer Vision, OpenCV, Deep Learning, TensorFlow, PyTorch, Image Processing',
                'benefits': 'Health insurance, Flexible work hours, Learning resources',
                'contact_email': 'careers@visionai.com'
            }
        ]

        for job_data in ai_jobs:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                company=job_data['company'],
                defaults=job_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created job: {job.title} at {job.company}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Job already exists: {job.title} at {job.company}')
                )

        self.stdout.write(
            self.style.SUCCESS('AI/Data Science jobs created successfully!')
        ) 