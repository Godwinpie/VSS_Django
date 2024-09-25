import os
import json
import  logging
from allauth.account import app_settings
from allauth.account.models import EmailAddress
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from urllib.parse import urlparse,quote

from .magento.encrypt import MagentoEncryptor
logger = logging.getLogger(__name__)
def require_email_confirmation():
    return settings.ACCOUNT_EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY


def user_has_confirmed_email_address(user, email):
    try:
        email_obj = EmailAddress.objects.get_for_user(user, email)
        return email_obj.verified
    except EmailAddress.DoesNotExist:
        return False


def validate_profile_picture(value):
    valid_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".tif",
        ".tiff",
        ".webp",
        ".svg",
        ".bmp",
    }
    file_extension = os.path.splitext(value.name)[1].lower()
    if file_extension not in valid_extensions:
        raise ValidationError(
            _("Please upload a valid image file! Supported types are {types}").format(
                types=", ".join(valid_extensions),
            )
        )
    max_file_size = 5242880  # 5 MB limit
    if value.size > max_file_size:
        size_in_mb = value.size // 1024**2
        raise ValidationError(
            _("Maximum file size allowed is 5 MB. Provided file is {size} MB.").format(
                size=size_in_mb,
            )
        )
def encrypt_data(data):
    encrypter = MagentoEncryptor()
    return quote(encrypter.encrypt(data), safe='')
def get_encrypted_user_data(user, next_url=None):
    hashed_password = user.password
    last_four = hashed_password[-4:]
    shop_customer_number = user.shop_customer_number
    if not shop_customer_number:
        raise RuntimeError(' Login is successful, but there is no shop customer number.')
    data = {
        'customer_id': user.shop_customer_number,
        'email': user.email,
        'is_logged_in': True,
        'last_four': last_four,
        'redirect_url': next_url,
    }
    return encrypt_data(json.dumps(data))
def is_sso_login_url(next_url):
    """
        Generates the Magento SSO login URL with encrypted user data if the next_url domain matches
        the Magento domain; otherwise, returns False.

        Args:
            user: The user object to be authenticated.
            next_url: The URL where the user will be redirected after login.

        Returns:
            str: The Magento SSO login URL with encrypted user data, or False if domains do not match.
        """
    if next_url == '/':
        return False
    magento_url = settings.MAGENTO_SSO_LOGIN_PATH
    logger.error(next_url)
    try:
        # Extract the domain from the provided next_url
        next_domain = urlparse(next_url).netloc
        # Extract the domain from the Magento SSO login path
        magento_domain = urlparse(magento_url).netloc
    except Exception as e:
        # Log the exception if needed
        return False

    # Check if the domains match
    if next_domain != magento_domain:
        # If domains match, return False as no SSO login is needed
        return False
    return magento_url

def get_magento_sso_login(user, next_url):
    magento_url = is_sso_login_url(next_url)
    if not magento_url:
        return False

    # If domains do not match, encrypt user data and create SSO login URL
    data = get_encrypted_user_data(user, next_url)
    data = quote(data, safe='')
    logger.info(magento_url)
    url =  f'{magento_url}?data={data}'
    return url
