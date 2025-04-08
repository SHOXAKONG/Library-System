from .base import Base
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomManager(models.Manager):
    def search(self, q):
        return self.get_queryset().filter(full_name__icontains=q)


class Author(Base):
    full_name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Date of Birth"))
    bio = models.TextField(null=True, blank=True, verbose_name=_("Bio"))

    objects = CustomManager()

    class Meta:
        db_table = 'author'
        permissions = [
            ('can_manage_author', "Can Manage Author"),
        ]
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


    def __str__(self):
        return self.full_name
