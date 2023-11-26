from django.db import models
from django.core import validators
from main_app.managers import AuthorManager


# Model Mixins
class TimeStampPublished(models.Model):
    class Meta:
        abstract = True

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )


# Regular Models
class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(3),
        ]
    )

    email = models.EmailField(
        unique=True,
    )

    is_banned = models.BooleanField(
        default=False,
    )

    birth_year = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1900),
            validators.MaxValueValidator(2005),
        ]
    )

    website = models.URLField(
        null=True,
        blank=True,
    )

    objects = AuthorManager()


class Article(TimeStampPublished):
    class CategoryTypes(models.TextChoices):
        Technology = 'Technology'
        Science = 'Science'
        Education = 'Education'

    title = models.CharField(
        max_length=200,
        validators=[
            validators.MinLengthValidator(5)
        ]
    )

    content = models.TextField(
        validators=[
            validators.MinLengthValidator(10),
        ]
    )

    category = models.CharField(
        max_length=10,
        choices=CategoryTypes.choices,
        default=CategoryTypes.Technology,
        validators=[
            validators.MaxLengthValidator(10),
        ]
    )

    authors = models.ManyToManyField(
        to=Author,
        related_name='authors_articles',
    )


class Review(TimeStampPublished):
    content = models.TextField(
        validators=[
            validators.MinLengthValidator(10),
        ]
    )

    rating = models.FloatField(
        validators=[
            validators.MinValueValidator(1.0),
            validators.MaxValueValidator(5.0),
        ]
    )

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='author_review',
    )

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='article_review',
    )
