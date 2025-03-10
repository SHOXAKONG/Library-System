from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .base import Base

def code_time():
    return timezone.now() + timedelta(minutes=10)

class Code(Base):
    code_number = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_user')
    expired_date = models.DateTimeField(default=code_time)