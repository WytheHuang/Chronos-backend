from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    """Chatbot app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "chatbot"

    def ready(self):  # noqa: D102
        from . import signals  # noqa: F401
