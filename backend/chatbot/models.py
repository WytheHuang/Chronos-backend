from django.db import models

from core.models import BaseModel


class Conversation(BaseModel):
    """Model representing a conversation with the chatbot.

    This model stores the details of a conversation with the chatbot, including the user's input and the chatbot's response.

    Attributes:
        name (CharField): The name of the conversation.
        record_file_s3_key (CharField): The S3 key of the conversation record file.
        state (CharField): The state of the conversation (PENDING or COMPLETE).

    """

    class State(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETE = "COMPLETE", "Complete"

    name = models.CharField(max_length=255, null=True, blank=True)
    record_file_s3_key = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=10, choices=State.choices, default=State.COMPLETE)

    class Meta:
        db_table = "conversation"

    def __str__(self) -> str:
        return f"Conversation {self.id}"


class Message(BaseModel):
    """Model representing a message in a conversation.

    This model stores the details of a message in a conversation, including the message text and the timestamp.

    Attributes:
        conversation_id (UUIDField): The unique identifier for the conversation associated with the message.
        text (TextField): The text of the message.
        type (CharField): The type of the message (USER or CHATBOT).

    """

    class Type(models.TextChoices):
        USER = "USER", "User"
        CHATBOT = "CHATBOT", "Chatbot"

    conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT, related_name="messages")
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.USER)
    text = models.TextField()

    class Meta:
        db_table = "message"

    def __str__(self) -> str:
        return f"Message {self.id}"
