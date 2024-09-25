from django.core.management.base import BaseCommand
from apps.norm.erp.norm import NormImporter

class Command(BaseCommand):
    help = 'Imports norms from the NAVISION API'

    def add_arguments(self, parser):
        parser.add_argument('--normno', type=str, help='The norm number to fetch')
        parser.add_argument('--fromdatetime', type=str, help='The datetime to fetch norms from (format: YYYY-MM-DDZHH:MMh)')

    def handle(self, *args, **kwargs):
        norm_no = kwargs.get('normno')
        from_datetime = kwargs.get('fromdatetime')

        importer = NormImporter()

        try:
            norm_data = importer.fetch_data(norm_no=norm_no, from_datetime=from_datetime)
        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return
        new = 0
        update = 0
        for norm_obj, created, error_message in importer.import_norm(norm_data):
            if error_message:
                self.stdout.write(self.style.ERROR(error_message))
            elif created:
                new += 1
                self.stdout.write(self.style.SUCCESS(f'Created new norm: {norm_obj}'))
            else:
                update += 1
                self.stdout.write(self.style.SUCCESS(f'Updated existing norm: {norm_obj}'))

        self.stdout.write(self.style.SUCCESS(f'Finished importing norm data. New: {new}, Update: {update}'))
