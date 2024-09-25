from django.test import TestCase
from apps.orders.models import SalesOrder, SalesOrderItem, SalesInvoice, SalesInvoiceItem
from apps.users.models import Customer
from datetime import datetime
from decimal import Decimal

class SalesOrderModelTest(TestCase):

    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(
            customer_number='CUST123',
            name='Test Customer'
        )

        # Create a sales order
        self.sales_order = SalesOrder.objects.create(
            order_number='ORDER123',
            customer=self.customer,
            reference='Ref123',
            order_date=datetime.now().date(),
            delivery_date=datetime.now().date(),
            amount=Decimal('100.00'),
            amount_inc_vat=Decimal('120.00'),
            currency_code='USD',
            credit_card_amount=Decimal('100.00')
        )

    def test_create_sales_order(self):
        # Check that the sales order was created correctly
        self.assertEqual(SalesOrder.objects.count(), 1)
        self.assertEqual(self.sales_order.order_number, 'ORDER123')
        self.assertEqual(self.sales_order.customer, self.customer)
        self.assertEqual(self.sales_order.amount, Decimal('100.00'))
        self.assertEqual(self.sales_order.amount_inc_vat, Decimal('120.00'))
        self.assertEqual(self.sales_order.currency_code, 'USD')
        self.assertEqual(str(self.sales_order), 'ORDER123')

    def test_update_sales_order(self):
        # Update the sales order
        self.sales_order.amount = Decimal('150.00')
        self.sales_order.save()
        self.sales_order.refresh_from_db()
        self.assertEqual(self.sales_order.amount, Decimal('150.00'))

    def test_delete_sales_order(self):
        # Delete the sales order
        self.sales_order.delete()
        self.assertEqual(SalesOrder.objects.count(), 0)


class SalesOrderItemModelTest(TestCase):

    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(
            customer_number='CUST123',
            name='Test Customer'
        )

        # Create a sales order
        self.sales_order = SalesOrder.objects.create(
            order_number='ORDER123',
            customer=self.customer,
            order_date=datetime.now().date(),
            delivery_date=datetime.now().date(),
            amount=Decimal('100.00'),
            amount_inc_vat=Decimal('120.00'),
            currency_code='USD',
            credit_card_amount=Decimal('100.00')
        )

        # Create a sales order item
        self.sales_order_item = SalesOrderItem.objects.create(
            sales_order=self.sales_order,
            order_number='ORDER123',
            customer_id='CUST123',
            item_id='ITEM123',
            description='Test Item',
            delivery_date=datetime.now().date(),
            quantity=Decimal('2.00'),
            open_quantity=Decimal('1.00'),
            price=Decimal('50.00'),
            line_discount=Decimal('5.00'),
            line_price=Decimal('95.00'),
            line_price_inc_vat=Decimal('114.00'),
            download=False,
            print_on_demand=False,
            logistic=True,
            line_no='10000'
        )

    def test_create_sales_order_item(self):
        # Check that the sales order item was created correctly
        self.assertEqual(SalesOrderItem.objects.count(), 1)
        self.assertEqual(self.sales_order_item.item_id, 'ITEM123')
        self.assertEqual(self.sales_order_item.description, 'Test Item')
        self.assertEqual(self.sales_order_item.quantity, Decimal('2.00'))
        self.assertEqual(self.sales_order_item.price, Decimal('50.00'))
        self.assertEqual(self.sales_order_item.logistic, True)
        self.assertEqual(str(self.sales_order_item), f"Item ITEM123 for Order {self.sales_order.id}")

    def test_update_sales_order_item(self):
        # Update the sales order item
        self.sales_order_item.quantity = Decimal('3.00')
        self.sales_order_item.save()
        self.sales_order_item.refresh_from_db()
        self.assertEqual(self.sales_order_item.quantity, Decimal('3.00'))

    def test_delete_sales_order_item(self):
        # Delete the sales order item
        self.sales_order_item.delete()
        self.assertEqual(SalesOrderItem.objects.count(), 0)


class SalesInvoiceModelTest(TestCase):

    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(
            customer_number='CUST123',
            name='Test Customer'
        )

        # Create a sales order
        self.sales_order = SalesOrder.objects.create(
            order_number='ORDER123',
            customer=self.customer,
            order_date=datetime.now().date(),
            delivery_date=datetime.now().date(),
            amount=Decimal('100.00'),
            amount_inc_vat=Decimal('120.00'),
            currency_code='USD',
            credit_card_amount=Decimal('100.00')
        )

        # Create a sales invoice
        self.sales_invoice = SalesInvoice.objects.create(
            order_number=self.sales_order,
            customer=self.customer,
            order_date=datetime.now().date(),
            invoice_date=datetime.now().date(),
            invoice_amount=Decimal('200.00'),
            invoice_amount_inc_vat=Decimal('240.00'),
            currency_code='EUR'
        )

    def test_create_sales_invoice(self):
        # Check that the sales invoice was created correctly
        self.assertEqual(SalesInvoice.objects.count(), 1)
        self.assertEqual(self.sales_invoice.order_number, self.sales_order)
        self.assertEqual(self.sales_invoice.customer, self.customer)
        self.assertEqual(self.sales_invoice.invoice_amount, Decimal('200.00'))
        self.assertEqual(self.sales_invoice.invoice_amount_inc_vat, Decimal('240.00'))
        self.assertEqual(self.sales_invoice.currency_code, 'EUR')

    def test_update_sales_invoice(self):
        # Update the sales invoice
        self.sales_invoice.invoice_amount = Decimal('250.00')
        self.sales_invoice.save()
        self.sales_invoice.refresh_from_db()
        self.assertEqual(self.sales_invoice.invoice_amount, Decimal('250.00'))

    def test_delete_sales_invoice(self):
        # Delete the sales invoice
        self.sales_invoice.delete()
        self.assertEqual(SalesInvoice.objects.count(), 0)


class SalesInvoiceItemModelTest(TestCase):

    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(
            customer_number='CUST123',
            name='Test Customer'
        )

        # Create a sales order
        self.sales_order = SalesOrder.objects.create(
            order_number='ORDER123',
            customer=self.customer,
            order_date=datetime.now().date(),
            delivery_date=datetime.now().date(),
            amount=Decimal('100.00'),
            amount_inc_vat=Decimal('120.00'),
            currency_code='USD',
            credit_card_amount=Decimal('100.00')
        )

        # Create a sales invoice
        self.sales_invoice = SalesInvoice.objects.create(
            order_number=self.sales_order,
            customer=self.customer,
            order_date=datetime.now().date(),
            invoice_date=datetime.now().date(),
            invoice_amount=Decimal('200.00'),
            invoice_amount_inc_vat=Decimal('240.00'),
            currency_code='EUR'
        )

        # Create a sales invoice item
        self.sales_invoice_item = SalesInvoiceItem.objects.create(
            sales_invoice=self.sales_invoice,
            customer=self.customer,
            item_id='ITEM123',
            description='Test Invoice Item',
            quantity=Decimal('1.00'),
            price=Decimal('150.00'),
            line_discount=Decimal('0.00'),
            line_price=Decimal('150.00'),
            line_price_inc_vat=Decimal('180.00'),
            download=False,
            print_on_demand=True,
            logistic=False,
            line_no='10001'
        )

    def test_create_sales_invoice_item(self):
        # Check that the sales invoice item was created correctly
        self.assertEqual(SalesInvoiceItem.objects.count(), 1)
        self.assertEqual(self.sales_invoice_item.item_id, 'ITEM123')
        self.assertEqual(self.sales_invoice_item.description, 'Test Invoice Item')
        self.assertEqual(self.sales_invoice_item.quantity, Decimal('1.00'))
        self.assertEqual(self.sales_invoice_item.price, Decimal('150.00'))
        self.assertEqual(self.sales_invoice_item.print_on_demand, True)

    def test_update_sales_invoice_item(self):
        # Update the sales invoice item
        self.sales_invoice_item.quantity = Decimal('2.00')
        self.sales_invoice_item.save()
        self.sales_invoice_item.refresh_from_db()
        self.assertEqual(self.sales_invoice_item.quantity, Decimal('2.00'))

    def test_delete_sales_invoice_item(self):
        # Delete the sales invoice item
        self.sales_invoice_item.delete()
        self.assertEqual(SalesInvoiceItem.objects.count(), 0)
