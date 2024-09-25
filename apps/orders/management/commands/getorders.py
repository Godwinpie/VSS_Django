from django.core.management.base import BaseCommand
from apps.orders.erp.order import SalesOrderAndItemImporter

class Command(BaseCommand):
    help = 'Fetch sales orders from a third-party API and import them into the SalesOrder model'

    def add_arguments(self, parser):
        parser.add_argument('--fromdatetime', type=str,
                            help='The datetime to fetch customers from (format: YYYY-MM-DDZHH:MMh)')

    def handle(self, *args, **kwargs):
        importer = SalesOrderAndItemImporter()
        from_datetime = kwargs.get('fromdatetime')

        try:
            sales_order_data = importer.fetch_sales_order_data(from_datetime=from_datetime)
        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        for sales_order_obj, created, error_message in importer.import_sales_orders(sales_order_data):
            if error_message:
                self.stdout.write(self.style.ERROR(error_message))
            elif created:
                self.stdout.write(self.style.SUCCESS(f'Created new sales order: {sales_order_obj.order_number}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated existing sales order: {sales_order_obj.order_number}'))

        self.stdout.write(self.style.SUCCESS('Finished importing sales orders.'))
