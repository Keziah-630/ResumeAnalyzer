from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from resumes.models import Resume
from jobs.models import Job
from matcher.models import JobMatch
from matcher.views import generate_job_matches

class Command(BaseCommand):
    help = 'Clear existing job matches and regenerate them with real job data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing job matches...')
        
        # Clear all existing matches
        JobMatch.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all existing matches'))
        
        # Get all users with resumes
        users_with_resumes = User.objects.filter(resume__isnull=False).distinct()
        
        if not users_with_resumes.exists():
            self.stdout.write(self.style.WARNING('No users with resumes found'))
            return
        
        # Get all active jobs
        active_jobs = Job.objects.filter(is_active=True)
        
        if not active_jobs.exists():
            self.stdout.write(self.style.WARNING('No active jobs found'))
            return
        
        self.stdout.write(f'Found {users_with_resumes.count()} users with resumes')
        self.stdout.write(f'Found {active_jobs.count()} active jobs')
        
        # Regenerate matches for each user
        total_matches_created = 0
        
        for user in users_with_resumes:
            user_resumes = Resume.objects.filter(user=user)
            self.stdout.write(f'Processing user: {user.username} ({user_resumes.count()} resumes)')
            
            for resume in user_resumes:
                # Generate matches for this resume
                generate_job_matches(user, resume)
                
                # Count matches created for this resume
                matches_count = JobMatch.objects.filter(user=user, resume=resume).count()
                total_matches_created += matches_count
                
                self.stdout.write(f'  - Resume "{resume.full_name}": {matches_count} matches created')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_matches_created} job matches'))
        self.stdout.write('Job matching regeneration completed!') 