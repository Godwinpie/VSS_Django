from django.core.management.base import BaseCommand
from apps.orders.erp.order import SalesOrderAndItemImporter

class Command(BaseCommand):
    help = 'Fetch sales orders from a third-party API and import them into the SalesOrder model'

    def handle(self, *args, **kwargs):
        importer = SalesOrderAndItemImporter()

        try:
            sale_order_item_data = importer.fetch_sales_order_item_data()
        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        for sales_order_item_obj, created, error_message in importer.import_sales_order_items(sale_order_item_data):
            if error_message:
                self.stdout.write(self.style.ERROR(error_message))
            elif created:
                self.stdout.write(self.style.SUCCESS(f'Created new sales order Item: {sales_order_item_obj.item_id}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated existing sales order Item: {sales_order_item_obj.item_id}'))

        self.stdout.write(self.style.SUCCESS('Finished importing sales order Item'))
