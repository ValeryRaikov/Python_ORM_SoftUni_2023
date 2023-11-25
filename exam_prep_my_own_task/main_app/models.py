# Task: Blog Management System

from django.db import models
from django.core import validators
from main_app.managers import AuthorManager


# Model Mixins
class PublicationTimeStamp(models.Model):
    class Meta:
        abstract = True

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )


# Regular models
class Author(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(2, "Name cannot be less than 2 symbols!"),
        ]
    )

    email = models.EmailField(
        unique=True,
    )

    bio = models.TextField(
        max_length=200,
        null=True,
        blank=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    objects = AuthorManager()

    def __str__(self):
        return f'Author -> ID: {self.pk}, Name: {self.name}.'


class Post(PublicationTimeStamp):
    title = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(1, "Title cannot be empty!"),
        ]
    )

    content = models.TextField()

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='author_post',
    )

    is_published = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'Post -> ID: {self.pk}, Title: {self.title}.'


class Comment(PublicationTimeStamp):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_comment',
    )

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='author_comment',
    )

    text = models.TextField()

    def __str__(self):
        return f'Comment -> ID: {self.pk}, to post: {self.post.title}.'


class Like(models.Model):
    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='author_like',
    )

    post = models.ForeignKey(
        to='Post',
        on_delete=models.CASCADE,
        related_name='post_like',
        null=True,
        blank=True,
    )

    comment = models.ForeignKey(
        to='Comment',
        on_delete=models.CASCADE,
        related_name='comment_like',
        null=True,
        blank=True,
    )

    date_liked = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'Like -> ID: {self.pk}, Author name: {self.author.name}.'
