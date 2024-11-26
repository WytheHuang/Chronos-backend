from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from ninja_jwt.authentication import AsyncJWTAuth
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.exceptions import AuthenticationFailed
from ninja_jwt.exceptions import InvalidToken
from ninja_jwt.settings import api_settings


class CustomJWTAuth(JWTAuth):
    """Custom JWT authentication class, for remove the avatar field from the user model."""

    def get_user(self, validated_token: dict) -> AbstractBaseUser:
        """Retrieve the user associated with the given validated token.

        Args:
            validated_token: The token that has been validated.

        Returns:
            AbstractBaseUser: The user associated with the token.

        Raises:
            InvalidToken: If the token does not contain a recognizable user identification.
            AuthenticationFailed: If the user is not found or is inactive.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError as e:
            raise InvalidToken(_("Token contained no recognizable user identification")) from e

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist as e:
            raise AuthenticationFailed(_("User not found")) from e

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"))

        return user


class CustomAsyncJWTAuth(AsyncJWTAuth, CustomJWTAuth):
    """Custom asynchronous JWT authentication class, for remove the avatar field from the user model."""
