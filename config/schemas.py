from core.models import User
from ninja import Schema
from ninja_jwt import schema
from ninja_jwt.tokens import AccessToken
from ninja_jwt.tokens import RefreshToken


class UserSchema(Schema):
    """User schema."""

    name: str
    email: str


class CompanySchema(Schema):
    """Company schema."""

    name: str


class TokenObtainPairOutputSchema(Schema):
    """Token obtain pair output schema."""

    access: str
    refresh: str
    user: UserSchema


class TokenObtainPairInputSchema(schema.TokenObtainInputSchemaBase):
    """Token obtain pair input schema."""

    @classmethod
    def get_response_schema(cls) -> type[Schema]:
        """Get response schema."""
        return TokenObtainPairOutputSchema

    @classmethod
    def get_token(cls, user: User) -> dict:
        """Get token."""
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        return {
            "access": str(access),
            "refresh": str(refresh),
            "user": {
                "name": user.name,
                "email": user.email,
            },
        }


class TokenRefreshOutputSchema(schema.TokenRefreshOutputSchema):
    """Token refresh output schema."""

    refresh: str
    access: str
    user: UserSchema


class TokenRefreshInputSchema(schema.TokenRefreshInputSchema):
    """Token refresh input schema."""

    @classmethod
    def get_response_schema(cls) -> type[Schema]:
        """Get response schema."""
        return TokenRefreshOutputSchema

    def to_response_schema(self) -> TokenObtainPairOutputSchema:
        """To response schema."""
        refresh = RefreshToken(self.refresh)
        try:
            user = User.objects.get(id=refresh.payload["user_id"])
        except User.DoesNotExist as e:
            raise Exception("User does not exist.") from e  # noqa: TRY002

        return TokenObtainPairOutputSchema(
            access=str(refresh.access_token),
            refresh=str(refresh),
            user={
                "name": user.name,
                "email": user.email,
            },
        )
