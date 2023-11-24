import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Create and run your queries within functions
from main_app.models import Director, Actor, Movie


# Django Queries I
def get_directors(search_name=None, search_nationality=None) -> str:
    if search_name is None and search_nationality is None:
        return ''

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = query_name & query_nationality
    elif search_name is not None:
        query = query_name
    elif search_nationality is not None:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    return '\n'.join([
        f"Director: {d.full_name}, "
        f"nationality: {d.nationality}, "
        f"experience: {d.years_of_experience}"
        for d in directors
    ])


def get_top_director() -> str:
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return '\n'.join([
        f"Top Director: {top_director.full_name}, movies: {top_director.num_movies}."
    ])


def get_top_actor() -> str:
    top_actor = Actor.objects.prefetch_related('starring_actor_movies').annotate(
        num_movies=Count('starring_actor_movies'),
        avg_rating=Avg('starring_actor_movies__rating'),
    ).order_by('-num_movies', 'full_name').first()

    if not top_actor or not top_actor.num_movies:
        return ''

    movies = ', '.join([m.title for m in top_actor.starring_actor_movies.all() if m])

    return '\n'.join([
        f"Top Actor: {top_actor.full_name}, "
        f"starring in movies: {movies}, movies average rating: "
        f"{top_actor.avg_rating:.1f}"
    ])


# Django Queries II
def get_actors_by_movies_count() -> str:
    actors = Actor.objects.annotate(
        num_movies=Count('actor_movies'),
    ).order_by('-num_movies', 'full_name')[:3]

    if not actors or not Movie.objects.all():
        return ''

    return '\n'.join([
        f"{a.full_name}, "
        f"participated in {a.num_movies} movies"
        for a in actors
    ])


def get_top_rated_awarded_movie() -> str:
    top_movie = Movie.objects \
        .select_related('starring_actor') \
        .prefetch_related('actors') \
        .filter(is_awarded=True) \
        .order_by('-rating', 'title') \
        .first()

    if not top_movie:
        return ''

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else "N/A"
    participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ', '.join(participating_actors)

    return (f"Top rated awarded movie: {top_movie.title}, "
            f"rating: {top_movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. "
            f"Cast: {cast}.")


def increase_rating() -> str:
    classic_movies_to_increase = (
        Movie.objects.filter(is_classic=True, rating__lt=10))

    if not classic_movies_to_increase:
        return "No ratings increased."

    num_updated_movies = classic_movies_to_increase.update(rating=F('rating') + 0.1)

    return f"Rating increased for {num_updated_movies} movies."
