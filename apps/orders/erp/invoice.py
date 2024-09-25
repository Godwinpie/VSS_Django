import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from apps.orders.models import SalesInvoice, SalesInvoiceItem
from apps.users.models import Customer
from apps.orders.models import SalesOrder
from datetime import datetime

class SalesInvoiceAndItemImporter:
    def __init__(self):
        self.url = settings.NAVISION_API_URL
        self.username = settings.NAVISION_USERNAME
        self.password = settings.NAVISION_PASSWORD

    def fetch_data(self, action, from_datetime='2024-01-01Z08:00h'):
        """Generic fetch function for both sales invoices and items based on the action parameter."""
        params = {'Action': action, 'fromdatetime': from_datetime}
        try:
            response = requests.get(self.url, params=params, auth=HTTPBasicAuth(self.username, self.password))
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'Error fetching data: {e}')

    def parse_date(self, date_str):
        """Parse a date string into a date object or return None if invalid."""
        return datetime.strptime(date_str, "%Y.%m.%d").date() if date_str not in ["", "0000.00.00"] else None

    def parse_decimal(self, value):
        """Parse a decimal value, returning 0.00 if invalid."""
        try:
            return float(value) if value else 0.00
        except ValueError:
            return 0.00

    def fetch_sales_invoice_data(self):
        """Fetch sales invoice data."""
        return self.fetch_data('GetInvoiceHead').get("InvoiceHeader", [])

    def import_sales_invoices(self, sales_invoices_data):
        """Import sales invoices."""
        for invoice in sales_invoices_data:
            try:
                sales_order = SalesOrder.objects.get(order_number=invoice.get('OrderNumber'))
            except SalesOrder.DoesNotExist:
                yield None, invoice.get("OrderNumber"), f'Sales order with OrderNumber {invoice.get("OrderNumber")} not found. Skipping invoice.'
                continue

            try:
                customer = Customer.objects.get(customer_number=invoice.get('CustomerID'))
            except Customer.DoesNotExist:
                yield None, invoice.get("CustomerID"), f'Customer with CustomerID {invoice.get("CustomerID")} not found. Skipping invoice.'
                continue

            order_date = self.parse_date(invoice.get('OrderDate'))
            invoice_date = self.parse_date(invoice.get('InvoiceDate'))

            sales_invoice_obj, created = SalesInvoice.objects.update_or_create(
                order_number=sales_order,
                defaults={
                    'customer': customer,
                    'reference': invoice.get('Reference', ''),
                    'order_date': order_date,
                    'invoice_date': invoice_date,
                    'invoice_amount': self.parse_decimal(invoice.get('InvoiceAmount')),
                    'invoice_amount_inc_vat': self.parse_decimal(invoice.get('InvoiceAmountIncVAT')),
                    'currency_code': invoice.get('CurrencyCode', ''),
                    'shop_ref': invoice.get('ShopRef', ''),
                    'shop_id': invoice.get('ShopID', ''),
                    'typo3_user_id': invoice.get('TYPO3userID', ''),
                    'typo3_user_id_sync': invoice.get('TYPO3userIDSync', ''),
                    'typo3_id': invoice.get('TYPO3ID', ''),
                    'person_no': invoice.get('PersonNo', ''),
                    'is_sync_to_erp': False,
                    'is_sync_to_shop': False,
                }
            )

            yield sales_invoice_obj, created, None

    def fetch_sales_invoice_item_data(self):
        """Fetch sales invoice item data."""
        return self.fetch_data('GetInvoiceLine').get("InvoiceLine", [])

    def import_sales_invoice_items(self, sales_invoice_items_data):
        """Import sales invoice items."""
        for item in sales_invoice_items_data:
            try:
                sales_invoice = SalesInvoice.objects.get(order_number__order_number=item.get('InvoiceNumber'))
            except SalesInvoice.DoesNotExist:
                yield None, item.get("InvoiceNumber"), f'Sales invoice with InvoiceNumber {item.get("InvoiceNumber")} not found. Skipping item.'
                continue

            try:
                customer = Customer.objects.get(customer_number=item.get('CustomerID'))
            except Customer.DoesNotExist:
                yield None, item.get("CustomerID"), f'Customer with CustomerID {item.get("CustomerID")} not found. Skipping item.'
                continue

            end_date = self.parse_date(item.get('Enddate'))

            sales_invoice_item_obj, created = SalesInvoiceItem.objects.update_or_create(
                sales_invoice=sales_invoice,
                line_no=item.get('LineNo'),
                defaults={
                    'customer': customer,
                    'item_id': item.get('ItemID'),
                    'description': item.get('Description'),
                    'quantity': self.parse_decimal(item.get('Quantity')),
                    'price': self.parse_decimal(item.get('Price')),
                    'line_discount': self.parse_decimal(item.get('LineDiscount')),
                    'line_price': self.parse_decimal(item.get('LinePrice')),
                    'line_price_inc_vat': self.parse_decimal(item.get('LinePriceIncVAT')),
                    'shop_ref': item.get('ShopRef', ''),
                    'shop_id': item.get('ShopID', ''),
                    'typo3_sales_id': item.get('TYPO3salesID', ''),
                    'typo3_user_id': item.get('TYPO3userID', ''),
                    'typo3_user_id_sync': item.get('TYPO3userIDSync', ''),
                    'typo3_id': item.get('TYPO3ID', ''),
                    'download': bool(int(item.get('Download', '0'))),
                    'print_on_demand': bool(int(item.get('PrintOnDemand', '0'))),
                    'logistic': bool(int(item.get('Logistic', '0'))),
                    'end_date': end_date,
                    'is_sync_to_erp': False,
                    'is_sync_to_shop': False,
                }
            )

            yield sales_invoice_item_obj, created, None
