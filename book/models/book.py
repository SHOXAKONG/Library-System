from django.db import models

from book.models.author import Author
from book.models.base import Base


class Book(Base):
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    about = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'book'