from django.core.management.base import BaseCommand
from apps.subscription.erp.subscription import SubscriptionImporter  # Import the SubscriptionImporter
from apps.subscription.models import Subscription


class Command(BaseCommand):
    help = 'Fetch subscription data from a third-party API and insert it into the database'
    def add_arguments(self, parser):
        parser.add_argument('--fromdatetime', type=str,
                            help='The datetime to fetch subscription from (format: YYYY-MM-DDZHH:MMh)')

    def handle(self, *args, **kwargs):
        from_datetime = kwargs.get('fromdatetime')
        importer = SubscriptionImporter()

        try:
            # Fetch data from the API using the importer
            subscription_data = importer.fetch_data(from_datetime)
        except RuntimeError as e:
            # Handle any errors that occur during the data fetch
            self.stdout.write(self.style.ERROR(f"Error fetching data: {str(e)}"))
            return

        # Import the fetched subscription data
        for subscription_obj, created, error_message in importer.import_subscription_data(subscription_data):
            if error_message:
                # If there was an error during import, display the error
                self.stdout.write(self.style.ERROR(f"Error: {error_message}"))
                continue

            if created:
                # Output a success message if a new subscription was created
                self.stdout.write(self.style.SUCCESS(f'Created new subscription: {subscription_obj.subscription_nr}'))
            else:
                # Output a success message if an existing subscription was updated
                self.stdout.write(self.style.SUCCESS(f'Updated existing subscription: {subscription_obj.subscription_nr}'))

        # Final message to indicate the import process is complete
        self.stdout.write(self.style.SUCCESS('Finished importing subscription data.'))
