from core.admin import BaseAdmin
from django.contrib import admin

from . import models


@admin.register(models.FileUploadLogModel)
class FileUploadLogAdmin(BaseAdmin):
    """FileUploadLogModelAdmin definition."""

    list_display = ("file_name", "category", "s3_key", "upload_by")
    search_fields = ("file_name", "category__name", "s3_key", "upload_by__username")
    list_filter = ("upload_by", "category")
    readonly_fields = ("file_name", "category", "s3_key", "upload_by")
    fieldsets = (
        (
            "File Info",
            {
                "fields": (
                    "file_name",
                    "category",
                    "s3_key",
                    "upload_by",
                ),
            },
        ),
    )


@admin.register(models.CategoryModel)
class CategoryAdmin(BaseAdmin):
    """CategoryModelAdmin definition."""

    list_display = ("name",)
    search_fields = ("name",)
    readonly_fields = ("name",)
    fieldsets = (
        (
            "Category Info",
            {
                "fields": ("name",),
            },
        ),
    )
