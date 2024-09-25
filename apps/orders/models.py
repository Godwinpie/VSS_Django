from django.db import models
from apps.users.models import Customer

# Abstract Base Classes

class BaseSalesOrder(models.Model):
    # Common fields
    reference = models.CharField(max_length=255, blank=True, null=True)
    order_date = models.DateField()
    delivery_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_inc_vat = models.DecimalField(max_digits=10, decimal_places=2)
    currency_code = models.CharField(max_length=3)
    shop_ref = models.CharField(max_length=100, blank=True, null=True)
    shop_id = models.CharField(max_length=10, blank=True, null=True)
    shop_shipping_number = models.CharField(max_length=100, blank=True, null=True)
    delivery_address_code = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    shipping_costs = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    credit_card_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saferpay_id = models.CharField(max_length=255, blank=True, null=True)
    web_customer_email = models.EmailField(blank=True, null=True)
    export_id = models.CharField(max_length=100, blank=True, null=True)
    person_no = models.CharField(max_length=100, blank=True, null=True)
    lines = models.JSONField(default=list, blank=True, null=True)
    is_sync_to_erp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This model will not create a table

    def __str__(self):
        return self.reference or f"Order on {self.order_date}"

class BaseSalesOrderItem(models.Model):
    # Common fields
    item_id = models.CharField(max_length=100)
    description = models.TextField()
    delivery_date = models.DateField(null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    open_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    line_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    line_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    line_price_inc_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    download = models.BooleanField(default=False)
    print_on_demand = models.BooleanField(default=False)
    logistic = models.BooleanField(default=False)
    shop_ref = models.CharField(max_length=100, blank=True, null=True)
    shop_id = models.CharField(max_length=100, blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    line_no = models.CharField(max_length=50, null=True, blank=True)
    is_sync_to_erp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This model will not create a table

    def __str__(self):
        return self.item_id

# ERP Models

class SalesOrder(BaseSalesOrder):
    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, to_field='customer_number', on_delete=models.CASCADE)
    typo3_user_id = models.CharField(max_length=100, blank=True, null=True)
    typo3_user_id_sync = models.CharField(max_length=100, blank=True, null=True)
    typo3_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'sales_order'

    def __str__(self):
        return self.order_number

class SalesOrderItem(BaseSalesOrderItem):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    typo3_sales_id = models.CharField(max_length=100, blank=True, null=True)
    typo3_user_id = models.CharField(max_length=100, blank=True, null=True)
    typo3_user_id_sync = models.CharField(max_length=100, blank=True, null=True)
    typo3_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'sales_order_item'

    def __str__(self):
        return f"Item {self.item_id} for Order {self.sales_order.order_number}"

# Shop System Models

class ShopSalesOrder(BaseSalesOrder):
    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(
        Customer,
        to_field='customer_number',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_sent_to_erp = models.BooleanField(default=False)
    shop_order_id = models.IntegerField(default=0)
    shop_customer_id = models.IntegerField(default=0, blank=True, null=True)
    shop_increment_id = models.CharField(max_length=100, blank=True, null=True)
    erp_order_id = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'shop_sales_order'

    def __str__(self):
        return self.order_number if self.order_number else 'Unknown Order'

class ShopSalesOrderItem(BaseSalesOrderItem):
    shop_sales_order = models.ForeignKey(ShopSalesOrder, on_delete=models.CASCADE, related_name='items')
    shop_item_id = models.IntegerField(default=0)
    erp_item_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'shop_sales_order_item'

    def __str__(self):
        return f"Item {self.item_id} for Shop Order {self.shop_sales_order.order_number}"


class SalesInvoice(models.Model):
    order_number = models.ForeignKey(SalesOrder, to_field='order_number', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, to_field='customer_number', on_delete=models.CASCADE)
    reference = models.CharField(max_length=255, blank=True, null=True)
    order_date = models.DateField()
    invoice_date = models.DateField()
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_amount_inc_vat = models.DecimalField(max_digits=10, decimal_places=2)
    currency_code = models.CharField(max_length=3)
    shop_ref = models.CharField(max_length=100, blank=True, null=True)
    shop_id = models.CharField(max_length=10, blank=True, null=True)
    typo3_user_id = models.CharField(max_length=100, blank=True, null=True)
    typo3_user_id_sync = models.CharField(max_length=100, blank=True, null=True)
    typo3_id = models.CharField(max_length=100, blank=True, null=True)
    person_no = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'sales_invoice'

    def __str__(self):
        return f"Invoice for Order {self.order_number.order_number}"


class SalesInvoiceItem(models.Model):
    sales_invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name='invoice_items')
    customer = models.ForeignKey(Customer, to_field='customer_number', on_delete=models.CASCADE)
    item_id = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    line_discount = models.DecimalField(max_digits=10, decimal_places=2)
    line_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_price_inc_vat = models.DecimalField(max_digits=10, decimal_places=2)
    shop_ref = models.CharField(max_length=100, blank=True, null=True)
    shop_id = models.CharField(max_length=100, blank=True, null=True)
    typo3_sales_id = models.CharField(max_length=100, blank=True, null=True)
    typo3_user_id = models.CharField(max_length=100, blank=True, null=True)
    typo3_user_id_sync = models.CharField(max_length=100, blank=True, null=True)
    typo3_id = models.CharField(max_length=100, blank=True, null=True)
    download = models.BooleanField(default=False)
    print_on_demand = models.BooleanField(default=False)
    logistic = models.BooleanField(default=False)
    end_date = models.DateField(null=True, blank=True)
    line_no = models.CharField(max_length=50)

    class Meta:
        db_table = 'sales_invoice_item'

    def __str__(self):
        return f"Item {self.item_id} for Invoice {self.sales_invoice.id}"
