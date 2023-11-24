from django.db import models
from django.core import validators
from main_app.managers import DirectorManager


# Abstract models:
class BasePerson(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            validators.MinLengthValidator(2),
            validators.MaxLengthValidator(120),
        ]
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )

    class Meta:
        abstract = True


class IsAwarded(models.Model):
    is_awarded = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True


class TimeStampUpdated(models.Model):
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


# Models:
class Director(BasePerson):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[
            validators.MinValueValidator(0),
        ]
    )

    def __str__(self):
        return f"Director: {self.full_name}"

    objects = DirectorManager()


class Actor(BasePerson, IsAwarded, TimeStampUpdated):
    def __str__(self):
        return f"Actor: {self.full_name}"


class Movie(IsAwarded, TimeStampUpdated):
    class GenreTypes(models.TextChoices):
        Action = 'Action'
        Comedy = 'Comedy'
        Drama = 'Drama'
        Other = 'Other'

    title = models.CharField(
        max_length=150,
        validators=[
            validators.MinLengthValidator(5),
            validators.MaxLengthValidator(150),
        ]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=GenreTypes.choices,
        default=GenreTypes.Other,
        validators=[
            validators.MaxLengthValidator(6),
        ]
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[
            validators.MinValueValidator(0.0),
            validators.MaxValueValidator(10.0),
        ]
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='director_movies',
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='starring_actor_movies'
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='actor_movies',
    )

    def __str__(self):
        return f"Movie: {self.title}"
