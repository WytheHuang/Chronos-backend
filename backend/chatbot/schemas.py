from ninja import ModelSchema
from ninja import Schema

from core.utils import BASE_CREATE_EXCLUDE_FIELD
from core.utils import BASE_EXCLUDE_FIELD
from core.utils import BASE_GET_EXCLUDE_FIELD
from core.utils import BASE_UPDATE_EXCLUDE_FIELD

from . import models


class GetConversationResponseSchema(ModelSchema):
    """Conversation response schema for GET method."""

    class Config:
        model = models.Conversation
        model_exclude = BASE_GET_EXCLUDE_FIELD


class CreateConversationSchema(ModelSchema):
    """Conversation schema for POST method."""

    class Config:
        model = models.Conversation
        model_exclude = BASE_CREATE_EXCLUDE_FIELD


class PutConversationSchema(ModelSchema):
    """Conversation schema for PUT method."""

    class Config:
        model = models.Conversation
        model_exclude = BASE_UPDATE_EXCLUDE_FIELD


class GetMessageResponseSchema(ModelSchema):
    """Message response schema for GET method."""

    class Config:
        model = models.Message
        model_exclude = BASE_GET_EXCLUDE_FIELD


class CreateMessageSchema(ModelSchema):
    """Message schema for POST method."""

    class Config:
        model = models.Message
        model_exclude = BASE_CREATE_EXCLUDE_FIELD


class PutMessageSchema(ModelSchema):
    """Message schema for PUT method."""

    class Config:
        model = models.Message
        model_exclude = ["conversation", *BASE_UPDATE_EXCLUDE_FIELD]


class MessageResponseSchema(ModelSchema):
    """Message response schema for GET method."""

    class Config:
        model = models.Message
        model_exclude = BASE_EXCLUDE_FIELD


class ChatbotStateResponseSchema(Schema):
    """Chatbot state response schema."""

    state: models.Conversation.State
