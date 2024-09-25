from django import forms

from apps.users.models import Customer


class HijackUserForm(forms.Form):
    user_pk = forms.ModelChoiceField(queryset=Customer.objects.order_by("email"), label="User to impersonate")
