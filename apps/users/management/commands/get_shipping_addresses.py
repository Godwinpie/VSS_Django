from django.core.management.base import BaseCommand
from apps.users.erp.customer_shipping_address import CustomerShippingAddressImporter

class Command(BaseCommand):
    help = 'Fetch Customer Shipping Addresses'


    def add_arguments(self, parser):
        parser.add_argument('--fromdatetime', type=str,
                            help='The datetime to fetch Address from (format: YYYY-MM-DDZHH:MMh)')
        parser.add_argument('--customerno', type=str,
                            help='Customer Number')

    def handle(self, *args, **kwargs):
        from_datetime = kwargs.get('fromdatetime')
        customer_no = kwargs.get('customerno')
        importer = CustomerShippingAddressImporter()

        try:
            # Fetch data from the API using the importer
            shipping_address_data = importer.fetch_data(from_datetime=from_datetime,customer_no=customer_no)
        except RuntimeError as e:
            # Handle any errors that occur during the data fetch
            self.stdout.write(self.style.ERROR(f"Error fetching data: {str(e)}"))
            return

        # Import the fetched person data
        for shipping_obj, created, error_message in importer.import_shipping_addresses(shipping_address_data):
            if error_message:
                # If there was an error during import, display the error
                self.stdout.write(self.style.ERROR(f"Error: {error_message}"))
                continue

            if created:
                # Output a success message if a new person was created
                self.stdout.write(self.style.SUCCESS(f'Created new shipping address: {shipping_obj}'))
            else:
                # Output a success message if an existing person was updated
                self.stdout.write(self.style.SUCCESS(f'Updated existing shipping address: {shipping_obj}'))

        # Final message to indicate the import process is complete
        self.stdout.write(self.style.SUCCESS('Finished importing Customer shipping address.'))
