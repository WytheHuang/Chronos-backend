from django.db.models import signals
from django.db.models.base import ModelBase
from django.dispatch import receiver

from core.models import User

from . import models


@receiver(signals.post_save, sender=models.Message)
def reply_message(
    sender: ModelBase,  # noqa: ARG001
    instance: models.Message,
    created: bool,  # noqa: FBT001
    **kwargs,  # noqa: ARG001, ANN003
):
    """Reply to a message in a conversation.

    Args:
        sender (ModelBase): The model class of the sender.
        instance (models.Message): The instance of the message.
        created (bool): A boolean indicating if the instance was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        conversation = instance.conversation
        if instance.type == models.Message.Type.USER:
            conversation.state = models.Conversation.State.PENDING
            conversation.save(User.objects.get(email="admin@email.com"))

            message_reply = models.Message(
                conversation=conversation,
                type=models.Message.Type.CHATBOT,
                text="Hello! How can I help you today?",
            )
            message_reply.save(User.objects.get(email="admin@email.com"))
        else:
            conversation.state = models.Conversation.State.COMPLETE
            conversation.save(User.objects.get(email="admin@email.com"))
