import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Create and run your queries within functions

from main_app.models import Author, Article


# populate_model_with_data(Author)
# populate_model_with_data(Article)
# populate_model_with_data(Review)


# print(Author.objects.get_authors_by_article_count())


# Django Queries I
def get_authors(search_name=None, search_email=None) -> str:
    if search_name is None and search_email is None:
        return ''

    query = Q()

    if search_name is not None and search_email is not None:
        query &= Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif search_name is not None:
        query &= Q(full_name__icontains=search_name)
    elif search_email is not None:
        query &= Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ''

    return '\n'.join(
        f'Author: {a.full_name}, email: {a.email}, '
        f'status: {"Banned" if a.is_banned else "Not Banned" }' for a in authors
    )


# # print(get_authors('Author 1'))
# # print(get_authors())
# # print(get_authors('Author 5', 'author 5'))


def get_top_publisher() -> str:
    author = Author.objects.get_authors_by_article_count().first()

    if not author or author.article_count == 0:
        return ''

    return f'Top Author: {author.full_name} with {author.article_count} published articles.'


# # print(get_top_publisher())


def get_top_reviewer() -> str:
    author = Author.objects.prefetch_related(
        'author_review'
    ).annotate(
        review_count=Count('author_review')
    ).order_by(
        '-review_count',
        'email',
    ).first()

    if not author or author.review_count == 0:
        return ''

    return f'Top Reviewer: {author.full_name} with {author.review_count} published reviews.'


# print(get_top_reviewer())


# Django queries II
def get_latest_article() -> str:
    latest_article = Article.objects.order_by('-published_on').first()

    if not latest_article:
        return ''

    authors = latest_article.authors.all().order_by('full_name')
    authors_names = ', '.join(author.full_name for author in authors)
    review_count = latest_article.article_review.count()
    avg_rating = latest_article.article_review.aggregate(avg_rating=Avg('rating')).get('avg_rating')
    avg_rating_formatted = f'{avg_rating:.2f}' if avg_rating is not None else '0.00'

    return (f"The latest article is: {latest_article.title}. "
            f"Authors: {authors_names}. "
            f"Reviewed: {review_count} times. "
            f"Average Rating: {avg_rating_formatted}.")


# print(get_latest_article())


def get_top_rated_article() -> str:
    top_article = Article.objects.annotate(
        avg_rating=Avg('article_review__rating'),
        review_count=Count('article_review')
    ).exclude(
        avg_rating__isnull=True
    ).order_by(
        '-avg_rating',
        'title',
    ).first()

    if not top_article or top_article.review_count == 0:
        return ''

    return (f'The top-rated article is: {top_article.title}, '
            f'with an average rating of {top_article.avg_rating:.2f}, '
            f'reviewed {top_article.review_count} times.')


# print(get_top_rated_article())


def ban_author(email=None) -> str:
    if email is None:
        return 'No authors banned.'

    try:
        author = Author.objects.get(email=email)
    except Author.DoesNotExist:
        return "No authors banned."

    num_reviews_to_delete = author.author_review.count()
    author.author_review.all().delete()
    author.is_banned = True

    author.save()

    return f'Author: {author.full_name} is banned! {num_reviews_to_delete} reviews deleted.'


# print(ban_author('Author 1'))
# print(ban_author('Author 7'))
# print(ban_author('Author 5'))
# print(ban_author())
