from django.core.management.base import BaseCommand
from resumes.models import Resume
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Create demo resumes for demo purposes.'

    def handle(self, *args, **options):
        names = [
            'Ravi Kumar', 'Priya Sharma', 'Amit Singh', 'Sneha Reddy', 'Vikram Patel',
            'Anjali Mehta', 'Rahul Das', 'Kavya Nair', 'Suresh Babu', 'Divya Jain'
        ]
        skills_list = [
            'Python, Django, SQL, HTML, CSS',
            'Java, Spring, Hibernate, MySQL',
            'JavaScript, React, Node.js, Express',
            'C++, Data Structures, Algorithms',
            'AWS, Docker, Kubernetes, Linux',
            'Machine Learning, Data Science, Pandas',
            'UI/UX, Figma, Adobe XD',
            'PHP, Laravel, MySQL',
            'Android, Kotlin, Java',
            'iOS, Swift, Objective-C'
        ]
        education = 'B.Tech in Computer Science, XYZ University, 2020'
        experience = 'Software Developer at ABC Corp (2020-2022)\nIntern at DEF Ltd (2019-2020)'
        for i in range(5):
            name = random.choice(names)
            email = f"{name.lower().replace(' ', '')}@example.com"
            phone = f"+91-9{random.randint(100000000, 999999999)}"
            github = f"https://github.com/{name.lower().replace(' ', '')}"
            linkedin = f"https://linkedin.com/in/{name.lower().replace(' ', '')}"
            skills = random.choice(skills_list)
            user = User.objects.order_by('?').first()
            resume = Resume.objects.create(
                user=user,
                full_name=name,
                email=email,
                phone=phone,
                github=github,
                linkedin=linkedin,
                skills=skills,
                education=education,
                experience=experience,
                resume_file='resumes/demo_resume.pdf'
            )
            self.stdout.write(self.style.SUCCESS(f'Created resume for: {name}'))
        self.stdout.write(self.style.SUCCESS('Demo resumes created successfully!')) 