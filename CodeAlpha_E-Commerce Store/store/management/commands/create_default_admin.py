import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates a default superuser account if none exists.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DEFAULT_ADMIN_USER', 'admin')
        email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin123!')

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.NOTICE('Superuser already exists. No action taken.'))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                f'User "{username}" already exists but is not a superuser. Please promote this account manually or choose a different username.'
            ))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(
            f'Default superuser "{username}" created with password "{password}".'
        ))
