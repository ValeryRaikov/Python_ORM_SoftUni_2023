from django.db import models
from django.db.models import Count, QuerySet


class AuthorManager(models.Manager):
    def get_active_authors_with_posts(self) -> QuerySet:
        return self.annotate(
            posts_count=Count('author_post')
        ).filter(
            posts_count__gte=1,
            author_post__is_published=True,
        ).order_by(
            '-posts_count',
        )

    def get_active_authors_with_comments(self) -> QuerySet:
        return self.annotate(
            comments_count=Count('author_comment')
        ).filter(
            comments_count__gte=1,
        ).order_by(
            '-comments_count',
        )

    def get_active_authors_with_likes(self) -> QuerySet:
        return self.annotate(
            likes_count=Count('author_like')
        ).filter(
            likes_count__gte=1,
        ).order_by(
            '-likes_count',
        )
