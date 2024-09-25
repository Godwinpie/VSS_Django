from django.forms import BaseForm
from django.forms.fields import BooleanField, DateField, DateTimeField


def set_form_fields_disabled(form: BaseForm, disabled: bool = True) -> None:
    """
    For a given form, disable (or enable) all fields.
    """
    for field in form.fields:
        form.fields[field].disabled = disabled


class DefaultBaseForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if type(self.fields[field]) != BooleanField:
                self.fields[field].widget.attrs[
                    "class"
                ] = "input input-bordered w-full"
