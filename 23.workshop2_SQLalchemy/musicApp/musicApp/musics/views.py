from django.http import HttpResponse
from django.shortcuts import render, redirect
from additional.session_decorator import session_decorator
from musicApp.musics.models import Album, Song
from musicApp.musics.forms import AlbumCreateForm, AlbumEditForm, AlbumDeleteForm, SongCreateForm
from musicApp.settings import session


# Create your views here.
@session_decorator(session)
def index(request):
    albums = session.query(Album).all()

    context = {
        'albums': albums,
    }

    return render(request, 'common/index.html', context)


@session_decorator(session)
def create_album(request):
    if request.method == 'GET':
        form = AlbumCreateForm()

        context = {
            'form': form,
        }

        return render(request, 'albums/create-album.html', context)

    elif request.method == 'POST':
        form = AlbumCreateForm(request.POST)

        if form.is_valid():
            new_album = Album(
                album_name=form.cleaned_data['album_name'],
                image_url=form.cleaned_data['image_url'],
                price=form.cleaned_data['price'],
            )

            session.add(new_album)

            return redirect('index')


@session_decorator(session)
def details_album(request, id):
    album = session.query(Album).filter(Album.id == id).first()

    context = {
        'album': album,
    }

    return render(request, 'albums/album-details.html', context)


@session_decorator(session)
def edit_album(request, id):
    album = session.query(Album).filter(Album.id == id).first()

    if request.method == 'GET':
        initial_data = {
            'album_name': album.album_name,
            'image_url': album.image_url,
            'price': album.price,
        }

        form = AlbumEditForm(initial=initial_data)

        context = {
            'form': form,
            'album': album,
        }

        return render(request, 'albums/edit-album.html', context)

    elif request.method == 'POST':
        form = AlbumEditForm(request.POST)

        if form.is_valid():
            album.album_name = form.cleaned_data['album_name'],
            album.image_url = form.cleaned_data['image_url'],
            album.price = form.cleaned_data['price'],

            return redirect('index')


@session_decorator(session)
def delete_album(request, id):
    album = session.query(Album).filter(Album.id == id).first()

    if request.method == 'GET':
        initial_data = {
            'album_name': album.album_name,
            'image_url': album.image_url,
            'price': album.price,
        }

        form = AlbumDeleteForm(initial=initial_data)

        for field in form.fields.values():
            field.widget.attrs['disabled'] = True

        context = {
            'form': form,
            'album': album,
        }

        return render(request, 'albums/delete-album.html', context)

    elif request.method == 'POST':
        form = AlbumDeleteForm(request.POST)

        if form.is_valid():
            session.delete(album)

        return redirect('index')


@session_decorator(session)
def create_song(request):
    if request.method == 'GET':
        form = SongCreateForm()

        context = {
            'form': form,
        }

        return render(request, 'songs/create-song.html', context)

    elif request.method == 'POST':
        form = SongCreateForm(request.POST, request.FILES)

        if form.is_valid():
            new_song = Song(
                song_name=form.cleaned_data['song_name'],
                album_id=form.cleaned_data['album'],
                music_file=request.FILES['music_file'].read()
            )

            session.add(new_song)

            return redirect('index')


# Additional functionality from the live demo
@session_decorator(session)
def play_song(request, album_id, song_id):
    song = session.query(Song).filter_by(
        id=song_id,
        album_id=album_id,
    ).first()

    album = session.query(Album).filter_by(
        id=album_id,
    ).first()

    context = {
        'song': song,
        'album': album,
    }

    return render(request, 'songs/play-song.html', context)


@session_decorator(session)
def serve_song(request, album_id, song_id):
    song = session.query(Song).filter_by(
        id=song_id,
        album_id=album_id,
    ).first()

    if not song:
        return HttpResponse('Song not found!', status=404)
    else:
        response = HttpResponse(song.music_file, content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(song.song_name)
        return response


# My own page
@session_decorator(session)
def view_creator(request):
    creator_name = 'Valery Raikov'

    context = {
        'creator_name': creator_name,
    }

    return render(request, 'creator/display-creator.html', context)
