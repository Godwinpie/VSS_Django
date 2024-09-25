from django.core.management.base import BaseCommand
from apps.orders.erp.invoice import SalesInvoiceAndItemImporter

class Command(BaseCommand):
    help = 'Fetch sales invoice items from a third-party API and import them into the SalesInvoiceItem model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fromdatetime',
            type=str,
            default='2024-01-01Z08:00h',
            help='Datetime to start fetching invoice items from, in the format "YYYY-MM-DDZHH:MMh".'
        )

    def handle(self, *args, **options):
        from_datetime = options['fromdatetime']
        importer = SalesInvoiceAndItemImporter()

        try:
            sales_invoice_item_data = importer.fetch_data('GetInvoiceLine', from_datetime).get("InvoiceLine", [])
        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        for sales_invoice_item_obj, created, error_message in importer.import_sales_invoice_items(sales_invoice_item_data):
            if error_message:
                self.stdout.write(self.style.ERROR(error_message))
            elif created:
                self.stdout.write(self.style.SUCCESS(f'Created new sales invoice item: {sales_invoice_item_obj.item_id} for Invoice {sales_invoice_item_obj.sales_invoice.id}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated existing sales invoice item: {sales_invoice_item_obj.item_id} for Invoice {sales_invoice_item_obj.sales_invoice.id}'))

        self.stdout.write(self.style.SUCCESS('Finished importing sales invoice items.'))
