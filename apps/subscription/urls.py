from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.subscription.views import SubscriptionViewSet

router = DefaultRouter()
router.register(r'', SubscriptionViewSet)  # Register the viewset at the root of this URL

urlpatterns = [
    path('', include(router.urls)),  # This will map to api/subscriptions/ in the main project URLs
]
