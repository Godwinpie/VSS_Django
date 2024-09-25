from django.core.management.base import BaseCommand
from apps.firm.erp.firm import FirmImporter


class Command(BaseCommand):
    help = 'Fetch firm data from a third-party API and insert it into the database'

    def add_arguments(self, parser):
        parser.add_argument('--fromdatetime', type=str,
                            help='The datetime to fetch customers from (format: YYYY-MM-DDZHH:MMh)')
    def handle(self, *args, **kwargs):
        from_datetime = kwargs.get('fromdatetime')
        importer = FirmImporter()

        try:
            firmperson_data = importer.fetch_data_firmperson(from_datetime)  # Updated method name
        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        for firm_obj, created, error_message in importer.import_firmperson(firmperson_data):
            if error_message:
                self.stdout.write(self.style.ERROR(error_message))
            elif created:
                self.stdout.write(self.style.SUCCESS(f'Created new firm: {firm_obj}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated existing firm: {firm_obj}'))

        self.stdout.write(self.style.SUCCESS('Finished importing firm data.'))