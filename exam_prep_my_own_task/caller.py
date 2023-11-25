import os
import django
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils import timezone
from datetime import timedelta

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Post, Comment, Like
from populate_db import populate_model_with_data

# Populate the already created db tables with random data

# populate_model_with_data(Author)
# populate_model_with_data(Post)
# populate_model_with_data(Comment)
# populate_model_with_data(Like)


# Test the custom manager functions

# print(Author.objects.get_active_authors_with_posts())
# print(Author.objects.get_active_authors_with_comments())
# print(Author.objects.get_active_authors_with_likes())


# Django Queries Part I

def get_author_posts(author_name=None, author_email=None) -> str:
    if author_name is None and author_email is None:
        return ''

    query = Q()

    if author_name is not None:
        query &= Q(name__iexact=author_name)
    elif author_email is not None:
        query &= Q(email__iexact=author_email)
    else:
        query &= Q(name__iexact=author_name) & Q(email__iexact=author_email)

    try:
        matching_authors = Author.objects.get(query)
    except ObjectDoesNotExist as e:
        return 'No authors match the given criteria: ' + str(e)

    matching_posts = Post.objects.filter(author=matching_authors)

    return '\n'.join(
        f'{str(post)} by {post.author.name}' for post in matching_posts
    )


# print('Author posts:\n')
# print(get_author_posts('Author 5'))
# print(get_author_posts('Author 11'))


def get_most_recent_comments(num_comments=None) -> str:
    if num_comments is None:
        return ''

    comments = Comment.objects.filter(
        post__is_published=True,
    ).order_by(
        '-publication_date',
    )[:num_comments]

    if not comments:
        return ''

    return '\n'.join(
        f'{str(comment)} Date: {comment.publication_date}' for comment in comments
    )


# print('Most recent comments:\n')
# print(get_most_recent_comments(5))
# print(get_most_recent_comments())


def get_published_posts_by_author(author_info=None) -> str:
    if author_info is None:
        return ''

    query = Q(name__icontains=author_info) | Q(email__icontains=author_info) | Q(bio__icontains=author_info)

    try:
        author = Author.objects.get(query)
    except ObjectDoesNotExist as e:
        return 'No authors match the given criteria: ' + str(e)
    except MultipleObjectsReturned as e:
        return 'More than one author matches the given criteria: ' + str(e)

    author_posts = Post.objects.filter(
        author=author,
        is_published=True,
    ).order_by(
        'publication_date',
    )

    if not author_posts:
        return ''

    return '\n'.join(
        f'{str(post)} by {post.author.name}' for post in author_posts
    )


# print('Published posts by author:')
# print(get_published_posts_by_author('Author 8'))
# print(get_published_posts_by_author('Author 1'))
# print(get_published_posts_by_author())


def get_author_with_most_post_likes() -> str:
    author_post_likes = Author.objects.annotate(
        post_likes_count=Count('author_post__post_like')
    ).order_by(
        '-post_likes_count',
        'name',
    ).first()

    if not author_post_likes:
        return ''

    return f'{author_post_likes.name} has {author_post_likes.post_likes_count} post likes.'


# print(get_author_with_most_post_likes())


def get_author_with_most_comment_likes() -> str:
    author_comment_likes = Author.objects.annotate(
        comment_likes_count=Count('author_comment__comment_like')
    ).order_by(
        '-comment_likes_count',
        'name',
    ).first()

    if not author_comment_likes:
        return ''

    return f'{author_comment_likes.name} has {author_comment_likes.comment_likes_count} comment likes.'


# print(get_author_with_most_comment_likes())


# Django Queries Part II

def get_author_comment_count(author_name=None) -> str:
    if author_name is None:
        return ''

    try:
        author = Author.objects.get(name__iexact=author_name)
    except ObjectDoesNotExist as e:
        return 'No author matches the criteria: ' + str(e)

    comment_count = author.author_comment.count()

    return f'Author {author.name} has {comment_count} comments.'


# print(get_author_comment_count('Author 4'))
# print(get_author_comment_count('Author 9'))
# print(get_author_comment_count())


def get_all_author_posts_count() -> str:
    authors = Author.objects.annotate(
            posts_count=Count('author_post')
        ).order_by(
            '-posts_count',
            'name'
        )

    if not authors:
        return ''

    total_posts_count = sum(author.posts_count for author in authors)

    return f'Total comments: {total_posts_count}\n' + '\n'.join(
        f'Author: {author.name} has {author.posts_count} posts written.' for author in authors
    )


# print(get_all_author_posts_count())


def publish_delete_post(post_title=None, action=None) -> str:
    if post_title is None or action is None:
        return ''

    try:
        post = Post.objects.get(title__iexact=post_title)
    except ObjectDoesNotExist as e:
        return 'No post matches the given criteria: ' + str(e)

    if action.lower() == 'publish' and not post.is_published:
        post.is_published = True
        post.save()
        return f'{post_title} published successfully.'

    elif action.lower() == 'delete' and post.is_published:
        post.is_published = False
        post.save()
        return f'{post_title} deleted successfully.'

    else:
        return 'Invalid'


# print(publish_delete_post('Post 1', 'publish'))
# print(publish_delete_post('Post 2', 'publish'))
# print(publish_delete_post('Post 7', 'delete'))
# print(publish_delete_post('Post 7', 'delete'))


def get_comments_by_author(author_name=None) -> str:
    if author_name is None:
        return ''

    comments = Comment.objects.filter(author__name__iexact=author_name)

    if not comments:
        return ''

    return f'Comments of {author_name} are:\n' + '\n'.join(
        f'{comment.text}' for comment in comments
    )


# print(get_comments_by_author('Author 1'))
# print(get_comments_by_author('Author 3'))
# print(get_comments_by_author('Author 7'))


def archive_old_posts(days_threshold=None) -> str:
    if days_threshold is None:
        return ''

    threshold_date = timezone.now() - timedelta(days=days_threshold)

    posts_to_archive = Post.objects.filter(
        is_published=True,
        publication_date__lte=threshold_date,
        post_comment__isnull=True
    )

    archived_count = posts_to_archive.update(is_published=False)

    return f'{archived_count} posts archived successfully.'


# print(archive_old_posts(30))
