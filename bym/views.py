from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Review
from .forms import AlbumForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlencode
import os

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'bym/signup.html', {'form': form})


def home(request):
    albums = Album.objects.all()
    context = {"albums": albums}
    return render(request, "bym/home.html", context)


def album_detail(request, id):
    album = get_object_or_404(Album, pk=id)
    reviews = Review.objects.filter(album=album).order_by("-id")

    form = ReviewForm()
    has_reviewed = False

    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, album=album).first()
        has_reviewed = user_review is not None

    if request.method == "POST":
        if not request.user.is_authenticated:
            # Redirect to login with ?next= to return after login
            login_url = f"{reverse('login')}?{urlencode({'next': request.path})}"
            return redirect(login_url)

        if has_reviewed:
            return redirect("album_detail", id=album.id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                user=request.user,
                album=album,
                rating=form.cleaned_data["rating"],
                review=form.cleaned_data["review"]
            )
            album.update_rating()
            return redirect("album_detail", id=album.id)

    context = {
        "album": album,
        "reviews": reviews,
        "form": form,
        "has_reviewed": has_reviewed
    }
    return render(request, "bym/album_detail.html", context)


def buy_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    if request.method == 'POST':
        if album.quantity > 0:
            album.sell()
            messages.success(request, f"You bought '{album.title}'.")
        else:
            messages.error(request, f"'{album.title}' is out of stock.")
        return redirect('album_detail', id=album.id)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Ensure user owns the review
    if review.user != request.user:
        return redirect("album_detail", id=review.album.id)

    album = review.album
    review.delete()

    # Recalculate album rating
    album.update_rating()

    return redirect("album_detail", id=album.id)


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
        # Save the file path before deleting the album
        if album.cover:
            cover_path = album.cover.path
            if os.path.exists(cover_path):
                os.remove(cover_path)

        album.delete()
    return redirect('admin_home')

