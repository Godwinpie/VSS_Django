from rest_framework import serializers
from apps.subscription.models import Subscription
from apps.users.models import Customer

class SubscriptionSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer'
    )

    class Meta:
        model = Subscription
        fields = [
            'customer_id',
            'subscription_nr',
            'subscription_code',
            'subscription_type',
            'date_start',
            'date_end',
            'runtime_start',
            'runtime_end',
            'free_of_charge',
            'read_only',
            'active'
        ]
