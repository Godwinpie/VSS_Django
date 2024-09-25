from django.core.management.base import BaseCommand
from apps.orders.erp.invoice import SalesInvoiceAndItemImporter

class Command(BaseCommand):
    help = 'Fetch sales invoices from a third-party API and import them into the SalesInvoice model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fromdatetime',
            type=str,
            default='2024-01-01Z08:00h',
            help='Datetime to start fetching invoices from, in the format "YYYY-MM-DDZHH:MMh".'
        )

    def handle(self, *args, **options):
        from_datetime = options['fromdatetime']
        importer = SalesInvoiceAndItemImporter()

        try:
            sales_invoice_data = importer.fetch_data('GetInvoiceHead', from_datetime).get("InvoiceHeader", [])
        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        for sales_invoice_obj, created, error_message in importer.import_sales_invoices(sales_invoice_data):
            if error_message:
                self.stdout.write(self.style.ERROR(error_message))
            elif created:
                self.stdout.write(self.style.SUCCESS(f'Created new sales invoice: {sales_invoice_obj.order_number.order_number}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated existing sales invoice: {sales_invoice_obj.order_number.order_number}'))

        self.stdout.write(self.style.SUCCESS('Finished importing sales invoices.'))
