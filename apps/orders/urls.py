from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SalesOrderViewSet, SalesOrderItemViewSet,
    SalesInvoiceViewSet, SalesInvoiceItemViewSet,
    ShopSalesOrderCreateAPIView
)

router = DefaultRouter()
router.register(r'order', SalesOrderViewSet)
router.register(r'order-item', SalesOrderItemViewSet)
router.register(r'invoice', SalesInvoiceViewSet)
router.register(r'invoice-item', SalesInvoiceItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('shop-orders/', ShopSalesOrderCreateAPIView.as_view(), name='shop_orders_create'),
]
