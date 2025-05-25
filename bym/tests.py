import io
from io import BytesIO
from PIL import Image
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .models import Album, Review, Author
from .forms import AlbumForm


class AlbumModelTest(TestCase):
    def test_album_string_representation(self):
        author = Author.objects.create(name="Author")
        album = Album(title="Test", author=author, year=2023, price=9.99, quantity=1, cover="cover.jpg")
        self.assertEqual(str(album), "Test by Author")

    def test_album_sell_reduces_quantity(self):
        author = Author.objects.create(name="Auth")
        album = Album.objects.create(title="SellMe", author=author, year=2022, price=10, quantity=5, cover="cover.jpg")
        album.sell()
        album.refresh_from_db()
        self.assertEqual(album.quantity, 4)

    def test_update_rating_no_reviews_sets_zero(self):
        author = Author.objects.create(name="Auth")
        album = Album.objects.create(title="NoReviews", author=author, year=2022, price=10, quantity=1, cover="cover.jpg")
        album.update_rating()
        self.assertEqual(album.rating, 0.0)


class ReviewModelTest(TestCase):
    def test_review_string_representation(self):
        user = User.objects.create_user(username="user1", password="pass")
        author = Author.objects.create(name="Author")
        album = Album.objects.create(title="Album", author=author, year=2020, price=8.0, quantity=1, cover="cover.jpg")
        review = Review.objects.create(user=user, album=album, rating=4, review="Nice")
        self.assertEqual(str(review), "Review of Album by user1")


class BusinessLogicTest(TestCase):
    def test_update_rating_calculates_correct_average(self):
        user1 = User.objects.create_user(username="u1", password="pass")
        user2 = User.objects.create_user(username="u2", password="pass")
        author = Author.objects.create(name="Auth")
        album = Album.objects.create(title="Test", author=author, year=2020, price=8.0, quantity=1, cover="cover.jpg")

        Review.objects.create(user=user1, album=album, rating=5, review="Great!")
        Review.objects.create(user=user2, album=album, rating=3, review="Okay.")

        album.update_rating()
        self.assertEqual(album.rating, 4.0)

    def test_rating_updates_when_review_deleted(self):
        user = User.objects.create_user("test", "test@example.com", "pass")
        author = Author.objects.create(name="Author")
        album = Album.objects.create(title="Test", author=author, year=2022, price=10, quantity=1, cover="cover.jpg")
        Review.objects.create(user=user, album=album, rating=4, review="Nice")
        album.update_rating()
        self.assertEqual(album.rating, 4.0)

        Review.objects.all().delete()
        album.update_rating()
        self.assertEqual(album.rating, 0.0)


class AlbumFormTest(TestCase):
    def generate_test_image(self, format='JPEG'):
        image = Image.new('RGB', (100, 100), color='red')
        byte_io = io.BytesIO()
        image.save(byte_io, format=format)
        byte_io.seek(0)
        return SimpleUploadedFile('test.jpg', byte_io.read(), content_type='image/jpeg')

    def test_album_form_creates_new_author(self):
        image = self.generate_test_image()

        # Submit form data with a new author name
        form = AlbumForm(data={
            'title': 'New Album',
            'year': 2023,
            'price': 10.0,
            'quantity': 5,
            'new_author': 'New Author'
        }, files={
            'cover': image
        })

        # Check form validity
        self.assertTrue(form.is_valid(), msg=form.errors)

        # Save the album
        album = form.save()

        # Validate that the new author was created and assigned
        self.assertEqual(album.author.name, 'New Author')
        self.assertTrue(Author.objects.filter(name='New Author').exists())

    def test_album_form_rejects_large_image(self):
        image = Image.new('RGB', (2000, 2000))
        byte_io = BytesIO()
        image.save(byte_io, 'JPEG')
        byte_io.seek(0)

        file_data = {'cover': SimpleUploadedFile("big.jpg", byte_io.read(), content_type="image/jpeg")}
        form_data = {'title': 'Oversized', 'new_author': 'AuthorX', 'year': 2022, 'price': 10.0, 'quantity': 1}
        form = AlbumForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())
        self.assertIn("cover", form.errors)


class AlbumDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="pass")
        self.author = Author.objects.create(name="B")
        self.album = Album.objects.create(title="A", author=self.author, year=2022, price=10, quantity=1, cover="cover.jpg")

    def test_album_detail_status_code(self):
        url = reverse('album_detail', args=[self.album.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_album_detail_contains_title(self):
        response = self.client.get(reverse('album_detail', args=[self.album.id]))
        self.assertContains(response, "A")

    def test_logged_in_user_can_submit_review(self):
        self.client.login(username="reviewer", password="pass")
        response = self.client.post(
            reverse('album_detail', args=[self.album.id]),
            {'rating': 5, 'review': 'Super!'}
        )
        self.assertEqual(response.status_code, 302)
        self.album.refresh_from_db()
        self.assertEqual(self.album.rating, 5.0)
        self.assertEqual(Review.objects.count(), 1)

    def test_prevent_duplicate_review(self):
        Review.objects.create(user=self.user, album=self.album, rating=4, review="Good")
        self.client.login(username="reviewer", password="pass")
        response = self.client.post(
            reverse('album_detail', args=[self.album.id]),
            {'rating': 5, 'review': 'Duplicate!'}
        )
        self.assertEqual(Review.objects.count(), 1)

    def test_unauthenticated_user_cannot_submit_review(self):
        response = self.client.post(reverse('album_detail', args=[self.album.id]), {
            'rating': 5,
            'review': 'Hacky review'
        })
        self.assertEqual(Review.objects.count(), 0)
        self.assertRedirects(response, f"/login/?next=/albums/{self.album.id}/")


class ReviewDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="deleter", password="pass")
        self.author = Author.objects.create(name="Auth")
        self.album = Album.objects.create(title="Del", author=self.author, year=2020, price=10, quantity=1, cover="img.jpg")
        self.review = Review.objects.create(user=self.user, album=self.album, rating=4, review="Nice")

    def test_review_deletion(self):
        self.client.login(username="deleter", password="pass")
        response = self.client.post(reverse('delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

