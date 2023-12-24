from django.db import models
from django.core import validators
from fruitipediaApp.fruits.validators import check_name_validity


# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
    )


class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[
            validators.MinLengthValidator(2, 'Minimum length is 2 characters!'),
            check_name_validity,
        ]
    )

    image_url = models.URLField()

    description = models.TextField()

    nutrition = models.TextField(
        null=True,
        blank=True,
    )
