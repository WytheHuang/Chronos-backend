from ninja import Schema


class Http400BadRequestSchema(Schema):
    """Base schema for 400 response."""

    detail: str = "Bad Request"


class Http401UnauthorizedSchema(Schema):
    """Base schema for 401 response."""

    detail: str = "Unauthorized"


class Http403ForbiddenSchema(Schema):
    """Base schema for 403 response."""

    detail: str = "Forbidden"


class Http404NotFoundSchema(Schema):
    """Base schema for 404 response."""

    detail: str = "Not Found"


class BaseResponseSchema(Schema):
    """Base schema for response."""

    msg: str


class UserLoginResponseSchema(Schema):
    """User login response schema."""

    email: str
    access: str
    refresh: str
    permission: str


class UserRigisterRequestSchema(Schema):
    """User register request schema."""

    email: str
    password: str
    password_confirm: str


class UserRigisterResponseSchema(Schema):
    """User register response schema."""

    email: str


class UserUpdateNameSchema(Schema):
    """User update request schema."""

    name: str
