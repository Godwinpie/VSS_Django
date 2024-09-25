from django.core.management.base import BaseCommand
from apps.users.erp.person import PersonImporter

class Command(BaseCommand):
    help = 'Fetch person data from a third-party API and insert it into the database'


    def add_arguments(self, parser):
        parser.add_argument('--fromdatetime', type=str,
                            help='The datetime to fetch customers from (format: YYYY-MM-DDZHH:MMh)')
        parser.add_argument('--personno', type=str,
                            help='Person number')

    def handle(self, *args, **kwargs):
        from_datetime = kwargs.get('fromdatetime')
        person_no = kwargs.get('personno')
        importer = PersonImporter()

        try:
            # Fetch data from the API using the importer
            person_data = importer.fetch_data(from_datetime=from_datetime,person_no=person_no)
        except RuntimeError as e:
            # Handle any errors that occur during the data fetch
            self.stdout.write(self.style.ERROR(f"Error fetching data: {str(e)}"))
            return

        # Import the fetched person data
        for person_obj, created, error_message in importer.import_person_data(person_data):
            if error_message:
                # If there was an error during import, display the error
                self.stdout.write(self.style.ERROR(f"Error: {error_message}"))
                continue

            if created:
                # Output a success message if a new person was created
                self.stdout.write(self.style.SUCCESS(f'Created new person: {person_obj}'))
            else:
                # Output a success message if an existing person was updated
                self.stdout.write(self.style.SUCCESS(f'Updated existing person: {person_obj}'))

        # Final message to indicate the import process is complete
        self.stdout.write(self.style.SUCCESS('Finished importing person data.'))
