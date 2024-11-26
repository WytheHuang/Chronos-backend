from typing import Any
from uuid import UUID

from django.core.handlers.wsgi import WSGIRequest
from ninja import Form
from ninja.files import UploadedFile
from ninja_extra import api_controller
from ninja_extra import route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from core import exceptions as core_exceptions
from core import schemas as core_schemas
from core import utils as core_utils
from core.models import BaseModel

from . import models
from . import schemas


conversation_crud_controller = core_utils.generate_crud_controller(
    model=models.Conversation,
    model_name="Conversation",
    controller_prefix="conversation",
    application_schemas=schemas,
)

message_crud_controller = core_utils.generate_crud_controller(
    model=models.Message,
    model_name="Message",
    controller_prefix="message",
    application_schemas=schemas,
)


@api_controller(
    prefix_or_class="chatbot",
    auth=JWTAuth(),
    tags=["chatbot"],
    permissions=[IsAuthenticated],
)
class ChatbotApiController:
    """Chatbot API controller."""

    @route.post(
        "",
        response={
            200: Any,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    def wip_new_chatbot(
        self,
        request: WSGIRequest,  # noqa: ARG002
        name: Form[str],  # noqa: ARG002
        file: UploadedFile,  # noqa: ARG002
    ) -> Any:
        """Create a new chatbot conversation."""
        return models.Conversation.objects.create()

    @route.get(
        "",
        response={
            200: list[schemas.GetConversationResponseSchema],
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    def list_chatbot(self, request: WSGIRequest):
        """List chatbot conversations."""
        return models.Conversation.objects.filter(created_by_user=request.user).values()

    @route.get(
        "/{conversation_id}",
        response={
            200: list[schemas.MessageResponseSchema],
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    def list_messages(
        self,
        request: WSGIRequest,  # noqa: ARG002
        conversation_id: UUID,
    ):
        """List messages in a chatbot conversation."""
        try:
            conversation = models.Conversation.objects.get(id=conversation_id)
        except models.Conversation.DoesNotExist as err:
            raise core_exceptions.Http404NotFoundException from err

        return models.Message.objects.filter(conversation=conversation).order_by("created_at").values()

    @route.post(
        "/{conversation_id}",
        response={
            200: schemas.MessageResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    def post_message(
        self,
        request: WSGIRequest,
        conversation_id: UUID,
        body: schemas.PutMessageSchema,
    ) -> BaseModel:
        """Post a message to a chatbot conversation."""
        try:
            conversation = models.Conversation.objects.get(id=conversation_id)
        except models.Conversation.DoesNotExist as err:
            raise core_exceptions.Http404NotFoundException from err

        message = models.Message(
            conversation=conversation,
            text=body.text,  # type: ignore
        )
        message.save(request.user)  # type: ignore

        return message

    @route.get(
        "/{conversation_id}/state",
        response={
            200: schemas.ChatbotStateResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    def get_chatbot_state(
        self,
        request: WSGIRequest,  # noqa: ARG002
        conversation_id: UUID,
    ) -> dict:
        """Get the state of the chatbot conversation."""
        try:
            conversation = models.Conversation.objects.get(id=conversation_id)
        except models.Conversation.DoesNotExist as err:
            raise core_exceptions.Http404NotFoundException from err

        return {"state": conversation.state}
