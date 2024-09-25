from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from apps.orders.models import SalesOrder, SalesOrderItem, SalesInvoice, SalesInvoiceItem
from apps.users.models import Customer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from datetime import datetime
from decimal import Decimal

# Get the custom user model
User = get_user_model()

class SalesOrderItemAPITest(APITestCase):

    def setUp(self):
        # Create a user and get authentication token using the custom user model
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

        # Set up the API client with token authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a customer and a sales order
        self.customer = Customer.objects.create(
            customer_number='CUST123',
            name='Test Customer'
        )
        self.sales_order = SalesOrder.objects.create(
            order_number='ORDER123',
            customer=self.customer,
            order_date=datetime.now().date(),
            delivery_date=datetime.now().date(),
            amount=100.00,
            amount_inc_vat=120.00,
            currency_code='USD',
            credit_card_amount=100.00
        )
        # Create a sales order item
        self.sales_order_item = SalesOrderItem.objects.create(
            sales_order=self.sales_order,
            order_number='ORDER123',
            customer_id='CUST123',
            item_id='ITEM123',
            description='Test Item',
            delivery_date=datetime.now().date(),
            quantity=2.00,
            open_quantity=1.00,
            price=50.00,
            line_discount=5.00,
            line_price=95.00,
            line_price_inc_vat=114.00,
            download=False,
            print_on_demand=False,
            logistic=True,
            line_no='10000'
        )
        self.sales_order_url = reverse('salesorder-list')
        self.sales_order_item_url = reverse('salesorderitem-list')

    def test_list_sales_order_items(self):
        response = self.client.get(self.sales_order_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Correctly handle the paginated response
        results = response.data.get('results', response.data)  # Handle paginated and non-paginated responses
        filtered_items = [item for item in results if item['item_id'] == 'ITEM123']
        self.assertEqual(len(filtered_items), 1)

    def test_create_sales_order_item(self):
        data = {
            'sales_order': self.sales_order.id,
            'order_number': 'ORDER124',
            'customer_id': 'CUST123',
            'item_id': 'ITEM124',
            'description': 'New Test Item',
            'delivery_date': datetime.now().date(),
            'quantity': 1.00,
            'open_quantity': 1.00,
            'price': 60.00,
            'line_discount': 10.00,
            'line_price': 50.00,
            'line_price_inc_vat': 55.00,
            'download': False,
            'print_on_demand': True,
            'logistic': True,
            'line_no': '10001'
        }
        response = self.client.post(self.sales_order_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SalesOrderItem.objects.count(), 2)
        self.assertEqual(SalesOrderItem.objects.get(item_id='ITEM124').description, 'New Test Item')

    def test_retrieve_sales_order_item(self):
        retrieve_url = reverse('salesorderitem-detail', args=[self.sales_order_item.id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item_id'], 'ITEM123')

    def test_update_sales_order_item(self):
        update_url = reverse('salesorderitem-detail', args=[self.sales_order_item.id])
        data = {
            'quantity': 3.00,
            'price': 55.00
        }
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sales_order_item.refresh_from_db()
        self.assertEqual(self.sales_order_item.quantity, 3.00)
        self.assertEqual(self.sales_order_item.price, 55.00)

    def test_delete_sales_order_item(self):
        delete_url = reverse('salesorderitem-detail', args=[self.sales_order_item.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SalesOrderItem.objects.count(), 0)

class SalesOrderAPITest(APITestCase):

    def setUp(self):
        # Create a user and get authentication token using the custom user model
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

        # Set up the API client with token authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a customer and a sales order
        self.customer = Customer.objects.create(
            customer_number='CUST123',
            name='Test Customer'
        )
        self.sales_order = SalesOrder.objects.create(
            order_number='ORDER123',
            customer=self.customer,
            order_date=datetime.now().date(),
            delivery_date=datetime.now().date(),
            amount=100.00,
            amount_inc_vat=120.00,
            currency_code='USD',
            credit_card_amount=100.00
        )
        self.sales_order_url = reverse('salesorder-list')

    def test_list_sales_orders(self):
        response = self.client.get(self.sales_order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Correctly handle the paginated response
        results = response.data.get('results', response.data)  # Handle paginated and non-paginated responses
        filtered_orders = [order for order in results if order['order_number'] == 'ORDER123']
        self.assertEqual(len(filtered_orders), 1)

    def test_create_sales_order(self):
        data = {
            'order_number': 'ORDER124',
            'customer': self.customer.customer_number,  # Make sure this matches the correct field type (primary key reference)
            'order_date': datetime.now().date(),
            'delivery_date': datetime.now().date(),
            'amount': 200.00,
            'amount_inc_vat': 240.00,
            'currency_code': 'EUR',
            'credit_card_amount': 200.00
        }
        response = self.client.post(self.sales_order_url, data, format='json')
        print(response.data)  # Print the response data to debug
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SalesOrder.objects.count(), 2)
        self.assertEqual(SalesOrder.objects.get(order_number='ORDER124').amount, 200.00)

    def test_retrieve_sales_order(self):
        retrieve_url = reverse('salesorder-detail', args=[self.sales_order.id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_number'], 'ORDER123')

    def test_update_sales_order(self):
        update_url = reverse('salesorder-detail', args=[self.sales_order.id])
        data = {
            'amount': 300.00,
            'currency_code': 'GBP'
        }
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sales_order.refresh_from_db()
        self.assertEqual(self.sales_order.amount, 300.00)
        self.assertEqual(self.sales_order.currency_code, 'GBP')

    def test_delete_sales_order(self):
        delete_url = reverse('salesorder-detail', args=[self.sales_order.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SalesOrder.objects.count(), 0)

class SalesInvoiceAPITest(APITestCase):

    def setUp(self):
        # Create a user and get authentication token using the custom user model
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

        # Set up the API client with token authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a customer, sales order, and sales invoice
        self.customer = Customer.objects.create(
            customer_number='CUST123',
            name='Test Customer'
        )
        self.sales_order = SalesOrder.objects.create(
            order_number='ORDER123',
            customer=self.customer,
            order_date=datetime.now().date(),
            delivery_date=datetime.now().date(),
            amount=100.00,
            amount_inc_vat=120.00,
            currency_code='USD',
            credit_card_amount=100.00
        )
        self.sales_invoice = SalesInvoice.objects.create(
            order_number=self.sales_order,
            customer=self.customer,
            order_date=datetime.now().date(),
            invoice_date=datetime.now().date(),
            invoice_amount=150.00,
            invoice_amount_inc_vat=180.00,
            currency_code='USD'
        )
        self.sales_invoice_url = reverse('salesinvoice-list')

    def test_list_sales_invoices(self):
        response = self.client.get(self.sales_invoice_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)  # Handle paginated and non-paginated responses
        filtered_invoices = [invoice for invoice in results if invoice['order_number'] == 'ORDER123']
        self.assertEqual(len(filtered_invoices), 1)

    def test_create_sales_invoice(self):
        data = {
            'order_number': self.sales_order.order_number,  # Ensure this points to an existing SalesOrder
            'customer': self.customer.customer_number,  # Use the correct identifier (customer_number for FK)
            'order_date': datetime.now().date(),
            'invoice_date': datetime.now().date(),
            'invoice_amount': '200.00',  # Ensure it matches the expected type (string or decimal)
            'invoice_amount_inc_vat': '240.00',
            'currency_code': 'EUR'
        }
        response = self.client.post(self.sales_invoice_url, data, format='json')
        print(response.data)  # Debug print to inspect errors
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SalesInvoice.objects.count(), 2)
        self.assertEqual(SalesInvoice.objects.get(invoice_amount=Decimal('200.00')).invoice_amount_inc_vat,
                         Decimal('240.00'))

    def test_retrieve_sales_invoice(self):
        retrieve_url = reverse('salesinvoice-detail', args=[self.sales_invoice.id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_number'], 'ORDER123')

    def test_update_sales_invoice(self):
        update_url = reverse('salesinvoice-detail', args=[self.sales_invoice.id])
        data = {
            'invoice_amount': 250.00,
            'currency_code': 'GBP'
        }
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sales_invoice.refresh_from_db()
        self.assertEqual(self.sales_invoice.invoice_amount, 250.00)
        self.assertEqual(self.sales_invoice.currency_code, 'GBP')

    def test_delete_sales_invoice(self):
        delete_url = reverse('salesinvoice-detail', args=[self.sales_invoice.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SalesInvoice.objects.count(), 0)

class SalesInvoiceItemAPITest(APITestCase):

    def setUp(self):
        # Create a user and get authentication token using the custom user model
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

        # Set up the API client with token authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a customer, sales order, sales invoice, and sales invoice item
        self.customer = Customer.objects.create(
            customer_number='CUST123',
            name='Test Customer'
        )
        self.sales_order = SalesOrder.objects.create(
            order_number='ORDER123',
            customer=self.customer,
            order_date=datetime.now().date(),
            delivery_date=datetime.now().date(),
            amount=100.00,
            amount_inc_vat=120.00,
            currency_code='USD',
            credit_card_amount=100.00
        )
        self.sales_invoice = SalesInvoice.objects.create(
            order_number=self.sales_order,
            customer=self.customer,
            order_date=datetime.now().date(),
            invoice_date=datetime.now().date(),
            invoice_amount=150.00,
            invoice_amount_inc_vat=180.00,
            currency_code='USD'
        )
        self.sales_invoice_item = SalesInvoiceItem.objects.create(
            sales_invoice=self.sales_invoice,
            customer=self.customer,
            item_id='ITEM123',
            description='Test Invoice Item',
            quantity=1.00,
            price=150.00,
            line_discount=0.00,
            line_price=150.00,
            line_price_inc_vat=180.00,
            download=False,
            print_on_demand=True,
            logistic=False,
            line_no='10001'
        )
        self.sales_invoice_item_url = reverse('salesinvoiceitem-list')

    def test_list_sales_invoice_items(self):
        response = self.client.get(self.sales_invoice_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)  # Handle paginated and non-paginated responses
        filtered_items = [item for item in results if item['item_id'] == 'ITEM123']
        self.assertEqual(len(filtered_items), 1)

    def test_create_sales_invoice_item(self):
        data = {
            'sales_invoice': self.sales_invoice.id,  # Ensure this points to an existing SalesInvoice
            'customer': self.customer.customer_number,  # Use the correct identifier (customer_number for FK)
            'item_id': 'ITEM124',
            'description': 'New Test Invoice Item',
            'quantity': '2.00',
            'price': '75.00',
            'line_discount': '5.00',
            'line_price': '70.00',
            'line_price_inc_vat': '84.00',
            'download': False,
            'print_on_demand': True,
            'logistic': False,
            'line_no': '10002'
        }
        response = self.client.post(self.sales_invoice_item_url, data, format='json')
        print(response.data)  # Debug print to inspect errors
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SalesInvoiceItem.objects.count(), 2)
        self.assertEqual(SalesInvoiceItem.objects.get(item_id='ITEM124').description, 'New Test Invoice Item')

    def test_retrieve_sales_invoice_item(self):
        retrieve_url = reverse('salesinvoiceitem-detail', args=[self.sales_invoice_item.id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item_id'], 'ITEM123')

    def test_update_sales_invoice_item(self):
        update_url = reverse('salesinvoiceitem-detail', args=[self.sales_invoice_item.id])
        data = {
            'quantity': 3.00,
            'price': 80.00
        }
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sales_invoice_item.refresh_from_db()
        self.assertEqual(self.sales_invoice_item.quantity, 3.00)
        self.assertEqual(self.sales_invoice_item.price, 80.00)

    def test_delete_sales_invoice_item(self):
        delete_url = reverse('salesinvoiceitem-detail', args=[self.sales_invoice_item.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SalesInvoiceItem.objects.count(), 0)
