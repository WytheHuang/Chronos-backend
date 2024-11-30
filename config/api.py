from django.http import HttpRequest
from ninja.openapi.docs import Redoc
from ninja_extra import NinjaExtraAPI

from config.auth import AuthController

from chatbot import apis as chatbot_apis
from core import apis as core_apis


api = NinjaExtraAPI(
    title="Chronos Backend",
    version="1.0.0",
    description="chronos backend",
    app_name="chronos-backend",
    docs=Redoc(),
    docs_url="docs/",
)


@api.get(
    "",
    tags=["health_check"],
)
async def api_root_health_check(request: HttpRequest):  # noqa: ARG001
    """Check api health."""
    return {"status": "healthy"}


@api.get(
    "health_check/",
    tags=["health_check"],
)
async def health_check(request: HttpRequest):  # noqa: ARG001
    """Check api health."""
    return {"status": "healthy"}


api.register_controllers(AuthController)

api.register_controllers(core_apis.UserEditController)

# api.register_controllers(chatbot_apis.conversation_crud_controller)
# api.register_controllers(chatbot_apis.message_crud_controller)
api.register_controllers(chatbot_apis.ChatbotApiController)
