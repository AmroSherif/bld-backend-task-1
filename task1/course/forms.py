from django import forms
from django.core.exceptions import ValidationError


def validate_length(value):
    length = len(value)
    if not (10 <= length <= 50):
        raise ValidationError(
            (
                "Invalid value, the length of the description must be between 10 and 50 characters"
            ),
            code="invalid_value",
        )


class CourseForms(forms.Form):
    name = forms.CharField(min_length=5, max_length=30)
    description = forms.CharField(validators=[validate_length])
