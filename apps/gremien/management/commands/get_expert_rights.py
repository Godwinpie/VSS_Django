from django.core.management.base import BaseCommand
from apps.gremien.erp.person_expert_right import PersonExpertRightImporter

class Command(BaseCommand):
    help = 'Fetch expert rights data from a third-party API and insert it into the database'

    def add_arguments(self, parser):
        parser.add_argument('--fromdatetime', type=str,
                            help='The datetime to fetch customers from (format: YYYY-MM-DDZHH:MMh)')

    def handle(self, *args, **kwargs):
        importer = PersonExpertRightImporter()
        from_datetime = kwargs.get('fromdatetime')
        try:
            # Fetch data from the API using the importer
            expert_rights_data = importer.fetch_data(from_datetime=from_datetime)
        except RuntimeError as e:
            # Handle any errors that occur during the data fetch
            self.stdout.write(self.style.ERROR(f"Error fetching data: {str(e)}"))
            return

        # Import the fetched expert rights data
        for expert_right_obj, created, error_message in importer.import_expert_rights_data(expert_rights_data):
            if error_message:
                # If there was an error during import, display the error
                self.stdout.write(self.style.ERROR(f"Error: {error_message}"))
                continue

            if created:
                # Output a success message if a new expert right was created
                self.stdout.write(self.style.SUCCESS(f'Created new expert right: {expert_right_obj}'))
            else:
                # Output a success message if an existing expert right was updated
                self.stdout.write(self.style.SUCCESS(f'Updated existing expert right: {expert_right_obj}'))

        # Final message to indicate the import process is complete
        self.stdout.write(self.style.SUCCESS('Finished importing expert rights data.'))
