# apps/order/management/commands/create_magento_user.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



class Command(BaseCommand):
    help = 'Get or create a token for a specific user by email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Email address of the user (required)',
        )
    def handle(self, *args, **options):
        email = options.get('email')

        # Validate that the email parameter is not empty
        if not email:
            self.stderr.write(self.style.ERROR('Error: The --email parameter cannot be empty.'))
            return

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Error: User with email '{email}' does not exist."))
            return
        # Generate or get the token for the Magento user
        token, created = Token.objects.get_or_create(user=user)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new token for user '{email}': {token.key}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Token for user '{email}' already exists: {token.key}"))

        # Important: Securely store the token and provide it to the Magento application
