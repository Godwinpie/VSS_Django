from django.contrib import admin
from .models import SalesOrder, ShopSalesOrder, ShopSalesOrderItem

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'order_date', 'amount', 'currency_code')
    search_fields = ('order_number', 'customer__customer_number', 'web_customer_email')
    list_filter = ('order_date', 'currency_code')

@admin.register(ShopSalesOrder)
class ShopSalesOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'is_sent_to_erp', 'shop_order_id', 'erp_order_id', 'order_date', 'amount', 'currency_code')
    search_fields = ('order_number', 'shop_order_id', 'erp_order_id')
    list_filter = ('order_date', 'is_sent_to_erp', 'currency_code')

@admin.register(ShopSalesOrderItem)
class ShopSalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ('shop_item_id', 'display_shop_order_id', 'erp_item_id', 'item_id', 'description', 'quantity', 'price')
    search_fields = ('shop_item_id', 'sales_order__shop_order_id', 'erp_item_id', 'item_id')
    list_filter = ('erp_item_id',)

    # Correct method to display the related `shop_order_id`
    def display_shop_order_id(self, obj):
        # Access the correct foreign key relationship
        return obj.shop_sales_order.shop_order_id if obj.shop_sales_order else None
    display_shop_order_id.admin_order_field = 'shop_sales_order__shop_order_id'
    display_shop_order_id.short_description = 'Shop Order ID'
