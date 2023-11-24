from django.db import models
from django.core import validators
from main_app.model_mixins import TimeCreation
from main_app.model_managers import ProfileManager


class Profile(TimeCreation):
    full_name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(2),
        ]
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15,
        help_text='This field is typically a string to accommodate various phone number formats.',
    )

    address = models.TextField(
        help_text='This field can store longer text, suitable for addresses.',
    )

    is_active = models.BooleanField(
        default=True,
    )

    creation_date = models.DateTimeField(
        auto_now=True,
    )

    objects = ProfileManager()


class Product(TimeCreation):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.01),
        ]
    )

    in_stock = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(0),
        ]
    )

    is_available = models.BooleanField(
        default=True,
    )


class Order(TimeCreation):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='profile_orders',
    )

    products = models.ManyToManyField(
        to=Product,
        related_name='products_orders',
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.01),
        ]
    )

    is_completed = models.BooleanField(
        default=False,
    )
