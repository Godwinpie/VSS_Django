from rest_framework import viewsets
from .models import Firm
from .serializers import FirmSerializer

class FirmViewSet(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
