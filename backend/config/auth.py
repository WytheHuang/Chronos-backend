import re
from asgiref.sync import sync_to_async
from typing import Any

from django import core
from core import exceptions as core_exceptions
from core import schemas as core_schemas
from core.models import User
from django.contrib.auth.hashers import make_password
from ninja import Form
from ninja import Schema
from ninja_extra import ControllerBase
from ninja_extra import api_controller
from ninja_extra import route
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings


schema = SchemaControl(api_settings)


@api_controller("/auth", tags=["auth"])
class AuthController(ControllerBase):
    """Authentication controller."""

    auto_import = False

    @route.post(
        "/obtain",
        response={
            200: core_schemas.UserLoginResponseSchema,
            400: core_schemas.Http400BadRequestSchema,
            401: core_schemas.Http401UnauthorizedSchema,
        },
        url_name="auth_login",
    )
    async def obtain_token(self, user_token: schema.obtain_pair_schema):  # type: ignore
        """Get user's token.

        Args:
            user_token (schema.obtain_pair_schema): user's email and password.

        Returns:
            type[Schema]: jwt refresh and access token.
        """
        await sync_to_async(user_token.check_user_authentication_rule)()
        try:
            user = await User.objects.aget(email=user_token.email)
        except User.DoesNotExist:
            raise core_exceptions.Http400BadRequestException("User not found")

        return {
            "permission": "admin" if user.is_staff or user.is_superuser else "user",
            **dict(await sync_to_async(user_token.to_response_schema)()),
        }

    @route.post(
        "/refresh",
        response=schema.obtain_pair_refresh_schema.get_response_schema(),
        url_name="auth_refresh_token",
    )
    async def refresh_token(self, refresh_token: schema.obtain_pair_refresh_schema) -> type[Schema]:  # type: ignore
        """Refresh user's token.

        Args:
            refresh_token (schema.obtain_pair_refresh_schema): refresh token.

        Returns:
            type[Schema]: refresh and access token.
        """
        return await sync_to_async(refresh_token.to_response_schema)()

    @route.post(
        "/verify",
        response={200: Schema},
        url_name="auth_verify_token",
    )
    async def verify_token(self, token: schema.verify_schema) -> type[Schema]:  # type: ignore
        """Verify user's token.

        Args:
            token (schema.verify_schema): access token.

        Returns:
            type[Schema]: verify token.
        """
        return await sync_to_async(token.to_response_schema)()

    @route.post(
        "/register",
        response={200: core_schemas.UserRigisterResponseSchema, 400: core_schemas.Http400BadRequestSchema},
        url_name="auth_register",
    )
    async def register_user(self, body: Form[core_schemas.UserRigisterRequestSchema]):  # type: ignore
        """Register user."""
        user = await sync_to_async(User.objects.filter)(email=body.email)

        if await sync_to_async(len)(user) > 0:
            raise core_exceptions.Http400BadRequestException("Email already exists")

        if body.password != body.password_confirm:
            raise core_exceptions.Http400BadRequestException("Password and confirm password must be the same")

        await sync_to_async(User.objects.create)(
            email=body.email,
            password=make_password(body.password),
        )

        return {"email": body.email}
