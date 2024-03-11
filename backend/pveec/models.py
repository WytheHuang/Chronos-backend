from pyexpat import model
from typing import ClassVar

from core.models import BaseModel
from core.models import User
from django.db import models


class CategoryModel(BaseModel):
    """Model definition for CategoryModel."""

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        """Meta definition for CategoryModel."""

        indexes: ClassVar = [
            models.Index(fields=["id"]),
        ]


class FileUploadLogModel(BaseModel):
    """Model definition for FileUploadLogModel."""

    file_name = models.CharField(max_length=255)
    s3_key = models.TextField()
    upload_by = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.UUIDField(default=None)

    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True)

    class Meta:
        """Meta definition for FileUploadLogModel."""

        indexes: ClassVar = [
            models.Index(fields=["s3_key"]),
            models.Index(fields=["upload_by"]),
        ]
