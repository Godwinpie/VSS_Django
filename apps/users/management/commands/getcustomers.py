from django.core.management.base import BaseCommand
from apps.users.erp.user import CustomerImporter


class Command(BaseCommand):
    help = 'Fetch customer data from a third-party API and insert it into the database'

    def add_arguments(self, parser):
        parser.add_argument('--fromdatetime', type=str,
                            help='The datetime to fetch customers from (format: YYYY-MM-DDZHH:MMh)')

    def handle(self, *args, **kwargs):
        from_datetime = kwargs.get('fromdatetime')

        importer = CustomerImporter()
        try:
            customer_data = importer.fetch_customer_data(from_datetime=from_datetime)
        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        for customer_obj, created, error_message in importer.import_customers(customer_data):
            if error_message:
                self.stdout.write(self.style.ERROR(error_message))
            elif created:
                self.stdout.write(self.style.SUCCESS(f'Created new customer: {customer_obj.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated existing customer: {customer_obj.username}'))

        self.stdout.write(self.style.SUCCESS('Customer data import completed successfully.'))
