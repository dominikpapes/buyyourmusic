from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.FloatField()
    quantity = models.IntegerField()
    cover = models.ImageField(upload_to='album_covers')
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def update_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            self.rating = sum(r.rating for r in reviews) / reviews.count()
        else:
            self.rating = 0.0
        self.save()

    def sell(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.save()


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=2000)

    def __str__(self):
        return f"Review of {self.album.title} by {self.user.username}"
