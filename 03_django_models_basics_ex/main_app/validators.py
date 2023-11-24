from django.core.exceptions import ValidationError


def validate_age(age):
    if age > 100:
        raise ValidationError("Age must be less than 100!")
