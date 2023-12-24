from django.core.exceptions import ValidationError


def check_name_validity(value):
    if not all(char.isalpha() for char in value):
        raise ValidationError('Fruit name should contain only letters!')
