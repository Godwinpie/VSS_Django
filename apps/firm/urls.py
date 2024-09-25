from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FirmViewSet

router = DefaultRouter()
router.register(r'firms', FirmViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
