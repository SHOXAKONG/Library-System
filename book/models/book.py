from django.db import models

from book.models.author import Author
from book.models.base import Base

class CustomManager(models.Manager):
    def search(self, q):
        return self.get_queryset().filter(title__icontains=q)

class Book(Base):
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    about = models.TextField(blank=True, null=True)
    isbn = models.IntegerField()
    published_date = models.DateField(auto_now=True)

    objects = CustomManager()

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.title
