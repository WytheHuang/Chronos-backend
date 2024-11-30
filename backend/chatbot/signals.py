from functools import partial

from django.db import transaction
from django.db.models import signals
from django.db.models.base import ModelBase
from django.dispatch import receiver

from core.models import User

from . import models
from . import tasks


@receiver(signals.post_save, sender=models.Message)
def message_post_save_signal(
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

            transaction.on_commit(
                partial(
                    tasks.reply_message.delay,
                    conversation_id=conversation.id,
                    message_id=instance.id,
                ),
            )
        else:
            conversation.state = models.Conversation.State.COMPLETE
            conversation.save(User.objects.get(email="admin@email.com"))
