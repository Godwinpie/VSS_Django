from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext
from apps.utils.timezones import get_timezones_display
from .helpers import validate_profile_picture
from .models import Customer, Person, CustomerShippingAddress


class CustomerChangeForm(UserChangeForm):
    email = forms.EmailField(label=gettext("Email"), required=True)
    language = forms.ChoiceField(label=gettext("Language"))
    timezone = forms.ChoiceField(label=gettext("Timezone"), required=False)

    class Meta:
        model = Customer
        fields = ("email", "first_name", "last_name", "language", "timezone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        timezone = self.fields.get("timezone")
        timezone.choices = get_timezones_display()
        if settings.USE_I18N and len(settings.LANGUAGES) > 1:
            language = self.fields.get("language")
            language.choices = settings.LANGUAGES
        else:
            self.fields.pop("language")


class UploadAvatarForm(forms.Form):
    avatar = forms.FileField(validators=[validate_profile_picture])


class PersonAddressForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "address", "address2", "postal_code", "city", "mobile_p"]


class CustomerShippingAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerShippingAddress
        fields = ["name", "name2", "address", "address2", "postal_code", "city"]

class UpdateLanguageForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['language_code']

    language_code = forms.ChoiceField(choices=settings.AVAILABLE_LANGUAGES, widget=forms.RadioSelect, label=gettext("Language"))


    def clean_language_code(self):
        language_code = self.cleaned_data.get('language_code')
        if language_code not in [lang[0] for lang in settings.AVAILABLE_LANGUAGES]:
            raise forms.ValidationError(gettext('Invalid language code. Please select a valid language.'))
        return language_code


