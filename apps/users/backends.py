from apps.subscription.models import Subscription
from allauth.account.auth_backends import AuthenticationBackend as AllauthAuthenticationBackend
import logging


logger = logging.getLogger(__name__)

class SubscriptionAuthenticationBackend(AllauthAuthenticationBackend):

    def authenticate(self, request, **credentials):
        # Log when the custom backend is called
        logger.info("SubscriptionAuthenticationBackend called")

        # Use the existing logic to authenticate the user
        user = super().authenticate(request, **credentials)

        # If the user is authenticated, check for the subscription condition
        if user and Subscription.objects.filter(
            customer=user,
            subscription_code=Subscription.SUBSCRIPTION_CODE_ALLOWED,
            active=True
        ).exists():
            # Log successful subscription check
            logger.info(f"User {user} passed subscription check.")
            # Return the user if the subscription is valid
            return user

        # Log failed subscription check
        logger.info(f"User {user} failed subscription check.")
        return None
