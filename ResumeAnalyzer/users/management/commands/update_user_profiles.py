from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile

class Command(BaseCommand):
    help = 'Update existing users with UserProfile objects'

    def handle(self, *args, **options):
        users = User.objects.all()
        created_count = 0
        updated_count = 0
        
        for user in users:
            if hasattr(user, 'profile'):
                # Update existing profile
                user.profile.is_regular_user = not (user.is_superuser or user.is_staff)
                user.profile.save()
                updated_count += 1
                self.stdout.write(f"Updated profile for user: {user.username}")
            else:
                # Create new profile
                is_regular = not (user.is_superuser or user.is_staff)
                UserProfile.objects.create(
                    user=user,
                    is_regular_user=is_regular
                )
                created_count += 1
                self.stdout.write(f"Created profile for user: {user.username}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {users.count()} users. '
                f'Created {created_count} profiles, updated {updated_count} profiles.'
            )
        ) 