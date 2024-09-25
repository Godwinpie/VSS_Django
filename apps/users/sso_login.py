from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import  logging

logger = logging.getLogger(__name__)


def sso_redirect(request):
    # Retrieve the referrer URL (Magento URL)
    referrer_url = request.GET.get('next', '/')

    # Store the referrer URL in session for later use
    request.session['next_url'] = referrer_url
    logger.info('test')

    # Redirect to the Django login page
    return redirect('account_login')


@login_required
def after_login_redirect(request):
    # Retrieve the stored referrer URL from session
    next_url = request.session.get('next_url', '/')

    # Clear the session to remove the stored referrer URL
    del request.session['next_url']
    logger.info(next_url)

    # Redirect the user to the referrer URL
    return redirect(next_url)
