
import  logging

from allauth.account.utils import send_email_confirmation
from allauth_2fa.utils import user_has_valid_totp_device
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


from .forms import CustomerChangeForm, UploadAvatarForm
from .helpers import require_email_confirmation, user_has_confirmed_email_address, get_magento_sso_login, encrypt_data
from .models import Customer

logger = logging.getLogger(__name__)
@login_required
def profile(request):
    if request.method == "POST":
        form = CustomerChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user_before_update = Customer.objects.get(pk=user.pk)
            need_to_confirm_email = (
                user_before_update.email != user.email
                and require_email_confirmation()
                and not user_has_confirmed_email_address(user, user.email)
            )
            if need_to_confirm_email:
                # don't change it but instead send a confirmation email
                # email will be changed by signal when confirmed
                new_email = user.email
                send_email_confirmation(request, user, signup=False, email=new_email)
                user.email = user_before_update.email
                # recreate the form to avoid populating the previous email in the returned page
                form = CustomerChangeForm(instance=user)
            user.save()

            user_language = user.language
            if user_language and user_language != translation.get_language():
                translation.activate(user_language)
            if user.timezone != timezone.get_current_timezone():
                if user.timezone:
                    timezone.activate(user.timezone)
                else:
                    timezone.deactivate()
            messages.success(request, _("Profile successfully saved."))
    else:
        form = CustomerChangeForm(instance=request.user)
    return render(
        request,
        "account/profile.html",
        {
            "form": form,
            "active_tab": "profile",
            "page_title": _("Profile"),
            "user_has_valid_totp_device": user_has_valid_totp_device(request.user),
            "now": timezone.now(),
            "current_tz": timezone.get_current_timezone(),
        },
    )

# custom login page
def sso_login_view(request):
    """
    Custom login view that checks for a valid subscription before logging in the user.
    """
    next_url = request.GET.get('next', '/')  # Replace '/default-url/' with your default URL
    logger.info(encrypt_data('testme'))

    # Check if the user is already logged in
    if request.user.is_authenticated:
        try:
            url = get_magento_sso_login(request.user, next_url)
        except  RuntimeError as e:
            messages.error(request, str(e))
            return redirect('/')
        logger.info(url)
        # Ensure URL is valid before redirecting
        if not url:
            return redirect('/')  # Fallback to a safe URL or handle the error accordingly
        return redirect(url)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            try:
                url = get_magento_sso_login(request.user, next_url)
            except  RuntimeError as e:
                messages.error(request, str(e))
                return redirect('/')
            if url:
                logger.info(url)
                return redirect(url)
            else:
                messages.info(request, "SSO Login")
                return redirect('/')
        else:
            # If authentication fails, display an error message
            messages.error(request, "Invalid login credentials or subscription not active.")

    return render(request, 'users/login.html', {'next': next_url})

@login_required
@require_POST
def upload_profile_image(request):
    user = request.user
    form = UploadAvatarForm(request.POST, request.FILES)
    if form.is_valid():
        user.avatar = request.FILES["avatar"]
        user.save()
        return HttpResponse(_("Success!"))
    else:
        readable_errors = ", ".join(str(error) for key, errors in form.errors.items() for error in errors)
        return JsonResponse(status=403, data={"errors": readable_errors})
