from django import forms

from apps.firm.models import FirmPerson, Firm
from apps.web.forms import DefaultBaseForm


class FirmPersonAddressForm(forms.ModelForm):
	class Meta:
		model = FirmPerson
		fields = ["name", "name2", "address", "address2", "postal_code", "city"]


class FirmAddressForm(DefaultBaseForm, forms.ModelForm):
	class Meta:
		model = Firm
		fields = ["name", "name2", "address", "address2", "postal_code", "city"]

