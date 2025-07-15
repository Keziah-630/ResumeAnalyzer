from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from resumes.models import Resume

class Command(BaseCommand):
    help = 'Create Sirisha user and demo resume with AI/Data Science background.'

    def handle(self, *args, **options):
        # Create Sirisha user if it doesn't exist
        sirisha_user, created = User.objects.get_or_create(
            username='sirisha',
            defaults={
                'first_name': 'Sirisha',
                'last_name': 'Reddy',
                'email': 'sirisha.reddy@example.com',
                'is_active': True,
            }
        )
        
        if created:
            sirisha_user.set_password('sirisha123')
            sirisha_user.save()
            self.stdout.write(self.style.SUCCESS('Created Sirisha user successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Sirisha user already exists.'))

        # Check if resume already exists for Sirisha
        if Resume.objects.filter(user=sirisha_user).exists():
            self.stdout.write(self.style.WARNING('Resume already exists for Sirisha. Skipping...'))
            return

        # Create demo resume for Sirisha
        resume = Resume.objects.create(
            user=sirisha_user,
            full_name='Sirisha Reddy',
            email='sirisha.reddy@example.com',
            phone='+91-9876543210',
            github='https://github.com/sirishareddy',
            linkedin='https://linkedin.com/in/sirishareddy',
            skills='Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, Matplotlib, SQL, Data Analysis, Natural Language Processing, Computer Vision, Neural Networks, Statistical Analysis, Data Visualization, Jupyter Notebook, Git, Docker, AWS, Google Cloud Platform',
            education='''Bachelor of Technology in Computer Science and Engineering
Specialization: Artificial Intelligence and Data Science
ABC University, Hyderabad
CGPA: 8.5/10
Graduation Year: 2024

Relevant Coursework:
- Machine Learning and Pattern Recognition
- Deep Learning and Neural Networks
- Data Mining and Analytics
- Natural Language Processing
- Computer Vision
- Big Data Analytics
- Statistical Methods for Data Science
- Database Management Systems''',
            experience='''Data Science Intern | TechCorp Solutions | June 2023 - August 2023
• Developed a machine learning model for customer churn prediction achieving 85% accuracy
• Implemented data preprocessing pipelines using Python and Pandas
• Created interactive dashboards using Tableau for business insights
• Collaborated with cross-functional teams to deploy ML models in production

AI Research Assistant | University AI Lab | January 2023 - May 2023
• Conducted research on transformer-based models for text classification
• Published paper on "Improving BERT Performance for Multi-label Classification"
• Implemented and evaluated various deep learning architectures
• Mentored junior students in machine learning concepts

Software Developer Intern | StartupXYZ | May 2022 - July 2022
• Built a recommendation system using collaborative filtering
• Developed REST APIs using Django and Django REST Framework
• Worked on frontend development using React.js
• Participated in agile development methodologies''',
            resume_file='resumes/sirisha_resume.pdf'
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created demo resume for Sirisha with AI/Data Science background!'
            )
        )
        self.stdout.write(f'Username: sirisha')
        self.stdout.write(f'Password: sirisha123')
        self.stdout.write(f'Resume ID: {resume.id}')
        self.stdout.write(f'Skills: {resume.skills[:100]}...') 