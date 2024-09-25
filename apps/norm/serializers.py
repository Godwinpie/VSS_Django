from rest_framework import serializers
from .models import Norm

class NormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Norm
        fields = '__all__'
