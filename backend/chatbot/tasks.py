from uuid import UUID

from config import celery_app

from core.models import User
from core.utils import OPENAI_CLIENT

from . import models


@celery_app.task
def reply_message(conversation_id: UUID, message_id: UUID):
    """Reply to a message in a conversation."""
    conversation = models.Conversation.objects.get(id=conversation_id)
    message = models.Message.objects.get(id=message_id)

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
        content=message.text,
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

    return message_reply.text
