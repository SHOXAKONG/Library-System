from django.db import models
from book.models.author import Author
from book.models.base import Base
from django.utils.translation import gettext_lazy as _


class CustomManager(models.Manager):
    def search(self, q):
        return self.get_queryset().filter(title__icontains=q)


class Book(Base):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name=_("Title"))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Author"))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Price'))
    about = models.TextField(blank=True, null=True, verbose_name=_("About"))
    isbn = models.IntegerField(verbose_name=_("ISBN"))
    published_date = models.DateField(auto_now=True, verbose_name=_("Published Date"))

    objects = CustomManager()

    class Meta:
        db_table = 'book'
        permissions = [
            ('can_manage_books', "Can Manage Books"),
        ]
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return self.title
