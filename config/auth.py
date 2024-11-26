import datetime

import pytz
from django.core.handlers.wsgi import WSGIRequest
from ninja_extra import ControllerBase
from ninja_extra import api_controller
from ninja_extra import route

from config.schemas import TokenObtainPairInputSchema
from config.schemas import TokenObtainPairOutputSchema
from config.schemas import TokenRefreshInputSchema
from config.schemas import TokenRefreshOutputSchema

from core.models import User


@api_controller("/auth", tags=["auth"])
class AuthController(ControllerBase):
    """Authentication controller."""

    auto_import = False

    @route.post(
        "/obtain",
        response=TokenObtainPairOutputSchema,
        url_name="auth_login",
    )
    def obtain_token(self, request: WSGIRequest, user_token: TokenObtainPairInputSchema):
        """Get user's token.

        Args:
            request (WSGIRequest): request object.
            user_token (schema.obtain_pair_schema): user's email and password.

        Returns:
            type[Schema]: jwt refresh and access token.
        """
        user_token.check_user_authentication_rule()

        login_time = datetime.datetime.now(pytz.timezone("Asia/Taipei"))

        ip_address = request.headers.get("x-forwarded-for")
        ip_address = ip_address.split(",")[0] if ip_address else request.META.get("REMOTE_ADDR")

        User.objects.filter(email=user_token._user.email).update(  # type: ignore # noqa: SLF001
            last_login_ip=ip_address,
            last_login_time=login_time,
        )

        return user_token.to_response_schema()

    @route.post(
        "/refresh",
        response=TokenRefreshOutputSchema,
        url_name="auth_refresh_token",
    )
    def refresh_token(self, refresh_token: TokenRefreshInputSchema):
        """Refresh user's token.

        Args:
            refresh_token (TokenRefreshInputSchema): refresh token.

        Returns:
            type[Schema]: refresh and access token.
        """
        return refresh_token.to_response_schema()

    # @route.post(
    #     "/verify",
    #     response={200: Schema},
    #     url_name="auth_verify_token",
    # )
    # def verify_token(self, token: schema.verify_schema) -> type[Schema]:
    #     """Verify user's token.

    #     Args:
    #         token (schema.verify_schema): access token.

    #     Returns:
    #         type[Schema]: verify token.
    #     """
    #     return token.to_response_schema()
