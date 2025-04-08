from django.db import models

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
