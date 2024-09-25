from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Basic serializer to pass Customer details to the front end.
    Extend with any fields your app needs.
    """

    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name", "email", "avatar_url", "get_display_name")
