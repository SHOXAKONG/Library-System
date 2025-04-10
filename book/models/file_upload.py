from .base import Base
from django.db import models
from .users import User

class FileUpload(Base):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    title = models.CharField(max_length=200)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('can_upload_file', "Can Upload File"),
            ('can_view_all_files', "Can View All Files")
        ]
