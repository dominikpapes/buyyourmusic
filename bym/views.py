from django.shortcuts import render, get_object_or_404, redirect
from .models import Album
from .forms import AlbumForm 

# Create your views here.

def home(request):
    albums = Album.objects.all()
    context = {"albums": albums}
    return render(request, "bym/home.html", context)


def album_detail(request, id):
    album = get_object_or_404(Album, pk=id)
    context = {
        "album": album,
        "reviews": [
            {
                "id": 1,
                "user": "user",
                "rating": 5,
                "review": "Written review"
            },
        ]
    }
    return render(request, "bym/album_detail.html", context)


def admin_home(request):
    albums = Album.objects.all()
    context = {
        "albums": albums
    }
    return render(request, "bym/admin_home.html", context)


def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = AlbumForm()
    return render(request, 'bym/album_form.html', {
        'form': form,
        'form_title': 'Add New Album',
        'submit_text': 'Create'
    })


def album_edit(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'bym/album_form.html', {
        'form': form,
        'form_title': 'Edit Album',
        'submit_text': 'Save Changes'
    })


def album_delete(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        album.delete()
        return redirect('admin_home')
    return render(request, 'bym/confirm_delete.html', {'album': album})