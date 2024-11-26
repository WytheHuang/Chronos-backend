from django.contrib import admin

from core.admin import BaseAdmin

from . import models


@admin.register(models.Conversation)
class ConversationAdmin(BaseAdmin):
    """Conversation inf admin UI built from django."""

    list_display = ["id", "name", "record_file_s3_key"]
    search_fields = ["name", "record_file_s3_key"]


@admin.register(models.Message)
class MessageAdmin(BaseAdmin):
    """Message inf admin UI built from django."""

    list_display = ["id", "conversation", "type", "text"]
    search_fields = ["conversation__name", "text"]
    list_filter = ["type"]
    list_select_related = ["conversation"]
