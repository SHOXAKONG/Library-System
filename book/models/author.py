from .base import Base
from django.db import models

class Author(Base):
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'author'
