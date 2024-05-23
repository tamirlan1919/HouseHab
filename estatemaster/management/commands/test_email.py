# estatemaster/management/commands/test_email.py

from django.core.mail import send_mail
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        try:
            send_mail(
                'Test Email',
                'This is a test email sent from Django.',
                'tchinchaev@bk.ru',
                ['tamirlan.chinchaev@gmail.com'],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Test email sent successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
