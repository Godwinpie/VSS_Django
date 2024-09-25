from rest_framework import viewsets
from rest_framework.permissions import AllowAny  # Adjust for testing
from .models import SalesOrder, SalesOrderItem, SalesInvoice, SalesInvoiceItem, ShopSalesOrder
from .serializers import SalesOrderSerializer, SalesOrderItemSerializer, SalesInvoiceSerializer, \
    SalesInvoiceItemSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShopSalesOrderSerializer
from rest_framework.permissions import IsAuthenticated  # For authentication



class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all().order_by('id')
    serializer_class = SalesOrderSerializer
    permission_classes = [AllowAny]  # Allow any user for testing purposes

class SalesOrderItemViewSet(viewsets.ModelViewSet):
    queryset = SalesOrderItem.objects.all().order_by('id')  # Adding ordering by 'id'
    serializer_class = SalesOrderItemSerializer
    permission_classes = [AllowAny]  # Adjust this as needed for your application


class SalesInvoiceViewSet(viewsets.ModelViewSet):
    queryset = SalesInvoice.objects.all().order_by('id')
    serializer_class = SalesInvoiceSerializer
    permission_classes = [AllowAny]  # Adjust this as needed for your application

class SalesInvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = SalesInvoiceItem.objects.all().order_by('id')
    serializer_class = SalesInvoiceItemSerializer
    permission_classes = [AllowAny]  # Adjust this as needed for your application



class ShopSalesOrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the request is authenticated
    def post(self, request):
        serializer = ShopSalesOrderSerializer(data=request.data)
        if serializer.is_valid():
            shop_sales_order = serializer.save()
            return Response(
                {
                    'message': 'Order created successfully',
                    'id': shop_sales_order.id
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        order_id = request.data.get('id')  # Get the order ID from the request data
        if not order_id:
            return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Attempt to find and delete the order
            order = ShopSalesOrder.objects.get(id=order_id)
            order.delete()
            return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ShopSalesOrder.DoesNotExist:
            # Handle case where the order does not exist
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

