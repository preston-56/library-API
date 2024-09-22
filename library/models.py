from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)  

    def __str__(self):
        return self.name

    @classmethod
    def get_author_id(cls, author_name):
        try:
            return cls.objects.get(name=author_name).id
        except cls.DoesNotExist:
            return None

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class Blacklist(models.Model):
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

