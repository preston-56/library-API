from .models import Author

def get_author_id(author_name):
    try:
        author = Author.objects.get(name=author_name)
        return author.id
    except Author.DoesNotExist:
        return None
