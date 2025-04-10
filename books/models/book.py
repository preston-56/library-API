from django.db import models
from authors.models.authors import Author

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'library_book'
    def __str__(self):
        return self.title