from rest_framework import serializers
from .models import SalesOrder, SalesOrderItem, SalesInvoice, SalesInvoiceItem
from .models import ShopSalesOrder, ShopSalesOrderItem

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = '__all__'

class SalesOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderItem
        fields = '__all__'  # Include all fields of SalesOrderItem
class SalesInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoice
        fields = '__all__'  # You can specify individual fields if needed

class SalesInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceItem
        fields = '__all__'  # You can specify individual fields if needed



class ShopSalesOrderItemSerializer(serializers.ModelSerializer):
    open_quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    line_discount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    line_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    line_price_inc_vat = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    line_no = serializers.CharField(max_length=50, required=False, allow_blank=True)

    class Meta:
        model = ShopSalesOrderItem
        fields = [
            'item_id',
            'description',
            'delivery_date',
            'quantity',
            'open_quantity',
            'price',
            'line_discount',
            'line_price',
            'line_price_inc_vat',
            'download',
            'print_on_demand',
            'logistic',
            'shop_ref',
            'shop_id',
            'end_date',
            'line_no',
            'is_sync_to_erp',
            'shop_item_id',
            'erp_item_id',
        ]

class ShopSalesOrderSerializer(serializers.ModelSerializer):
    items = ShopSalesOrderItemSerializer(many=True)
    credit_card_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)

    class Meta:
        model = ShopSalesOrder
        fields = [
            'order_number',
            'reference',
            'order_date',
            'delivery_date',
            'amount',
            'amount_inc_vat',
            'currency_code',
            'shop_ref',
            'shop_id',
            'shop_customer_id',
            'shop_shipping_number',
            'delivery_address_code',
            'comment',
            'shipping_costs',
            'credit_card_amount',
            'saferpay_id',
            'web_customer_email',
            'export_id',
            'person_no',
            'lines',
            'is_sync_to_erp',
            'is_sent_to_erp',
            'shop_order_id',
            'shop_increment_id',
            'erp_order_id',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        shop_sales_order = ShopSalesOrder.objects.create(**validated_data)
        for item_data in items_data:
            ShopSalesOrderItem.objects.create(shop_sales_order=shop_sales_order, **item_data)
        return shop_sales_order