from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Album, Review


class AlbumModelTest(TestCase):
    def test_album_string_representation(self):
        album = Album(title="Test", author="Author", year=2023, price=9.99, cover="cover.jpg")
        self.assertEqual(str(album), "Test by Author")


class ReviewModelTest(TestCase):
    def test_review_string_representation(self):
        user = User.objects.create_user(username="user1", password="pass")
        album = Album.objects.create(title="Album", author="Author", year=2020, price=8.0, cover="cover.jpg")
        review = Review.objects.create(user=user, album=album, rating=4, review="Nice")
        self.assertEqual(str(review), "Review of Album by user1")


class BusinessLogicTest(TestCase):
    def test_update_rating_calculates_correct_average(self):
        user1 = User.objects.create_user(username="u1", password="pass")
        user2 = User.objects.create_user(username="u2", password="pass")
        album = Album.objects.create(title="Test", author="Auth", year=2020, price=8.0, cover="cover.jpg")

        Review.objects.create(user=user1, album=album, rating=5, review="Great!")
        Review.objects.create(user=user2, album=album, rating=3, review="Okay.")

        album.update_rating()
        self.assertEqual(album.rating, 4.0)


class AlbumDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="pass")
        self.album = Album.objects.create(title="A", author="B", year=2022, price=10, cover="cover.jpg")

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
        self.assertEqual(response.status_code, 302)  # redirect
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
        self.assertEqual(Review.objects.count(), 1)  # still only one


class ReviewDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="deleter", password="pass")
        self.album = Album.objects.create(title="Del", author="Auth", year=2020, price=10, cover="img.jpg")
        self.review = Review.objects.create(user=self.user, album=self.album, rating=4, review="Nice")

    def test_review_deletion(self):
        self.client.login(username="deleter", password="pass")
        response = self.client.post(reverse('delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

