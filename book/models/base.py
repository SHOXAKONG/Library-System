from django.db import models
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    created_at = models.DateTimeField(auto_now=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True
