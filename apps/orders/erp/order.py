import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from apps.orders.models import SalesOrder, SalesOrderItem
from apps.users.models import Customer
from datetime import datetime
from apps.users.erp.user import get_customer
import  logging

from vss.base_erp_importer import BaseImporter

logger = logging.getLogger(__name__)

class SalesOrderAndItemImporter(BaseImporter):
    def fetch_sales_order_data(self,from_datetime=None):
        params = {
            'Action': 'GetSalesOrder',
            'fromdatetime': self.get_from_datetime(from_datetime)
        }
        return self.request(params=params).get("SalesHeader", [])

    def import_sales_orders(self, sales_orders_data):
        """import sales orders."""
        for order in sales_orders_data:
            try:
                customer = Customer.objects.get(customer_number=order.get('CustomerID'))
            except Customer.DoesNotExist:
                newCustomer = get_customer(order.get('CustomerID'))
                if newCustomer:
                    customer = newCustomer
                else:
                    yield None, order.get("OrderNumber"), f'Customer with ID {order.get("CustomerID")} not found. Skipping order.'
                    continue

            order_date = self.parse_date(order.get('OrderDate'))
            delivery_date = self.parse_date(order.get('DeliveryDate'))

            sales_order_obj, created = SalesOrder.objects.update_or_create(
                order_number=order.get('OrderNumber'),
                defaults={
                    'customer': customer,
                    'reference': order.get('Reference', ''),
                    'order_date': order_date,
                    'delivery_date': delivery_date,
                    'amount': self.parse_decimal(order.get('Amount')),
                    'amount_inc_vat': self.parse_decimal(order.get('AmountIncVAT')),
                    'currency_code': order.get('CurrencyCode', ''),
                    'shop_ref': order.get('ShopRef', ''),
                    'shop_id': order.get('ShopID', ''),
                    'shop_shipping_number': order.get('ShopShipingNumber', ''),
                    'delivery_address_code': order.get('DeliveryAdressCode', ''),
                    'typo3_user_id': order.get('TYPO3userID', ''),
                    'typo3_user_id_sync': order.get('TYPO3userIDSync', ''),
                    'typo3_id': order.get('TYPO3ID', ''),
                    'comment': order.get('Comment', ''),
                    'shipping_costs': self.parse_decimal(order.get('ShippingCosts')),
                    'credit_card_amount': self.parse_decimal(order.get('CreditCardAmount')),
                    'saferpay_id': order.get('SaferPayID', ''),
                    'web_customer_email': order.get('WebCustomerEmail', ''),
                    'export_id': order.get('ExportID', ''),
                    'person_no': order.get('PersonNo', ''),
                    'lines': order.get('lines', [])
                }
            )

            yield sales_order_obj, created, None

    def fetch_sales_order_item_data(self):
        params = {
            'Action': 'GetSalesLine'
        }
        return self.request(params).get("SalesLine", [])

    def import_sales_order_items(self,sales_order_items_data):
        """Fetch and import sales order items."""
        for item in sales_order_items_data:
            try:
                sales_order = SalesOrder.objects.get(order_number=item.get('OrderNumber'))
            except SalesOrder.DoesNotExist:
                yield None, item.get("OrderNumber"), f'Sales order with OrderNumber {item.get("OrderNumber")} not found. Skipping item.'
                continue

            try:
                customer = Customer.objects.get(customer_number=item.get('CustomerID'))
            except Customer.DoesNotExist:
                yield None, item.get("CustomerID"), f'Customer with CustomerID {item.get("CustomerID")} not found. Skipping item.'
                continue

            delivery_date = self.parse_date(item.get('DeliveryDate'))
            end_date = self.parse_date(item.get('Enddate'))

            sales_order_item_obj, created = SalesOrderItem.objects.update_or_create(
                sales_order=sales_order,
                line_no=item.get('LineNo'),
                defaults={
                    'order_number': item.get('OrderNumber'),
                    'customer_id': customer.customer_number,  # Linking to customer by customer_number
                    'item_id': item.get('ItemID'),
                    'description': item.get('Description'),
                    'delivery_date': delivery_date,
                    'quantity': self.parse_decimal(item.get('Quantity')),
                    'open_quantity': self.parse_decimal(item.get('OpenQuantity')),
                    'price': self.parse_decimal(item.get('Price')),
                    'line_discount': self.parse_decimal(item.get('LineDiscount')),
                    'line_price': self.parse_decimal(item.get('LinePrice')),
                    'line_price_inc_vat': self.parse_decimal(item.get('LinePriceIncVAT')),
                    'download': bool(int(item.get('Download', '0'))),
                    'print_on_demand': bool(int(item.get('PrintOnDemand', '0'))),
                    'logistic': bool(int(item.get('Logistic', '0'))),
                    'shop_ref': item.get('ShopRef', ''),
                    'shop_id': item.get('ShopID', ''),
                    'typo3_sales_id': item.get('TYPO3salesID', ''),
                    'typo3_user_id': item.get('TYPO3userID', ''),
                    'typo3_user_id_sync': item.get('TYPO3userIDSync', ''),
                    'typo3_id': item.get('TYPO3ID', ''),
                    'end_date': end_date,
                    'is_sync_to_erp': False,
                    'is_sync_to_shop': False,
                }
            )

            yield sales_order_item_obj, created, None
