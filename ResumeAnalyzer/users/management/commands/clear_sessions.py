from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Clear all sessions to resolve session conflicts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Clear sessions for specific user only',
        )

    def handle(self, *args, **options):
        if options['user']:
            # Clear sessions for specific user
            try:
                user = User.objects.get(username=options['user'])
                sessions = Session.objects.filter(expire_date__gte=timezone.now())
                user_sessions = []
                
                for session in sessions:
                    if session.get_decoded().get('_auth_user_id') == str(user.id):
                        user_sessions.append(session)
                
                count = len(user_sessions)
                for session in user_sessions:
                    session.delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully cleared {count} sessions for user "{user.username}"'
                    )
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User "{options["user"]}" not found')
                )
        else:
            # Clear all sessions
            count = Session.objects.count()
            Session.objects.all().delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully cleared all {count} sessions'
                )
            ) 