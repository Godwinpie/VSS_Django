from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.norm.views import NormViewSet

router = DefaultRouter()
router.register(r'norms', NormViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
