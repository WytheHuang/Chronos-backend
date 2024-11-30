from django.conf import settings
from django.db.models import signals
from django.db.models.base import ModelBase
from django.dispatch import receiver
from openai import OpenAI

from core.models import User

from . import models


OPENAI_CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)


@receiver(signals.post_save, sender=models.Conversation)
def start_conversation(
    sender: ModelBase,  # noqa: ARG001
    instance: models.Conversation,
    created: bool,  # noqa: FBT001
    **kwargs,  # noqa: ARG001, ANN003
):
    """Start a conversation.

    Args:
        sender (ModelBase): The model class of the sender.
        instance (models.Conversation): The instance of the conversation.
        created (bool): A boolean indicating if the instance was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        assistant = OPENAI_CLIENT.beta.assistants.create(
            name=instance.name,
            instructions="",
            model="gpt-4o-2024-11-20",
        )
        instance.assistant_id = assistant.id
        instance.save(User.objects.get(email="admin@email.com"))


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

            if conversation.assistant_id is None:
                assistant = OPENAI_CLIENT.beta.assistants.create(
                    name=conversation.name,
                    instructions="",
                    model="gpt-4o-2024-11-20",
                )
                conversation.assistant_id = assistant.id
                conversation.save(User.objects.get(email="admin@email.com"))

            thread = OPENAI_CLIENT.beta.threads.create()
            message_from_user = OPENAI_CLIENT.beta.threads.messages.create(  # noqa: F841
                thread_id=thread.id,
                role="user",
                content=instance.text,
            )

            run = OPENAI_CLIENT.beta.threads.runs.create_and_poll(
                assistant_id=conversation.assistant_id,
                thread_id=thread.id,
            )

            if run.status == "completed":
                latest_messages = OPENAI_CLIENT.beta.threads.messages.list(thread_id=thread.id).data[0]

                message_reply = models.Message(
                    conversation=conversation,
                    type=models.Message.Type.CHATBOT,
                    text=latest_messages.content[0].text.value,  # type: ignore
                )
                message_reply.save(User.objects.get(email="admin@email.com"))
        else:
            conversation.state = models.Conversation.State.COMPLETE
            conversation.save(User.objects.get(email="admin@email.com"))
