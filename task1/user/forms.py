from multiprocessing import Value
from django import forms
import unicodedata
from django.core.exceptions import ValidationError


def validate_password(value):
    if not {"Ll", "Lu", "Nd"}.issubset(unicodedata.category(ch) for ch in value):
        raise ValidationError(
            (
                "Invalid value, your password must have lower and upper case characters, digits and underscores"
            ),
            code="invalid_value",
        )


class UserForms(forms.Form):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    birth_date = forms.DateField()
    email = forms.EmailField()
    password = forms.CharField(max_length=100, validators=[validate_password])
