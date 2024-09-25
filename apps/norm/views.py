from rest_framework import viewsets
from .models import Norm
from .serializers import NormSerializer

class NormViewSet(viewsets.ModelViewSet):
    queryset = Norm.objects.all()
    serializer_class = NormSerializer
