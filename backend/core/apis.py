from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from ninja_extra import api_controller
from ninja_extra import route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from core import schemas as core_schemas

from . import schemas


@api_controller(
    prefix_or_class="user",
    auth=JWTAuth(),
    tags=["edit user"],
    permissions=[IsAuthenticated],
)
class UserEditController:
    """User edit controller."""

    @route.put(
        "",
        response={
            200: schemas.UserUpdateNameSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    def edit_user(
        self,
        request: WSGIRequest,
        body: schemas.UserUpdateNameSchema,
    ) -> Any:
        """Edit user information."""
        user = request.user

        user.name = body.name  # type: ignore
        user.save()

        return user
