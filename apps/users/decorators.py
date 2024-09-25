from django.shortcuts import redirect
from functools import wraps  # Import wraps to maintain view metadata
from apps.subscription.models import Subscription

def subscription_required(view_func):
    """
    Decorator for views that checks that the user has a valid subscription.
    """
    @wraps(view_func)  # Maintain original view function's metadata
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and has a valid subscription
        if request.user.is_authenticated and Subscription.objects.filter(
            customer=request.user,
            subscription_code=Subscription.SUBSCRIPTION_CODE_ALLOWED,
            active=True
        ).exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Adjust the redirect target as needed

    return _wrapped_view
