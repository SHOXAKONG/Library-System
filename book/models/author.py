from .base import Base
from django.db import models

class CustomManager(models.Manager):
    def search(self, q):
        return self.get_queryset().filter(full_name__icontains=q)

class Author(Base):
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    objects = CustomManager()

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.full_name