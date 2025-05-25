from django.db import models


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
    cover = models.ImageField(upload_to='album_covers')
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.title} by {self.author}"


class BymUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.username}"


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BymUser, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=2000)

    def __str__(self):
        return f"Review of {self.album.title} by {self.user.username}"
