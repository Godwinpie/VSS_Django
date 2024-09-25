from rest_framework import viewsets
from apps.subscription.models import Subscription
from apps.subscription.serializers import SubscriptionSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
