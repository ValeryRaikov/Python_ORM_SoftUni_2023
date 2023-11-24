import re

from django.core.exceptions import ValidationError


def is_name_valid(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError("Name can only contain letters and spaces")


def is_phone_number_valid(value):
    if not re.match(r'^\+359\d{9}$', value):
        raise ValidationError("Phone number must start with a '+359' followed by 9 digits")
