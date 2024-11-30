from types import ModuleType
from uuid import UUID

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.db.utils import IntegrityError
from ninja_extra import api_controller
from ninja_extra import route
from ninja_extra.permissions import IsAuthenticated
from openai import OpenAI

from core.authentication import CustomJWTAuth
from core.models import BaseModel

from . import exceptions
from . import schemas


OPENAI_CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_crud_controller(
    model: type[BaseModel],
    model_name: str,
    controller_prefix: str,
    application_schemas: ModuleType,
):
    """Generate a CRUD controller for a model.

    Args:
        model (type[BaseModel]): The model for which to generate the CRUD controller.
        model_name (str): The name of the model.
        controller_prefix (str): The prefix for the controller.
        application_schemas (ModuleType): The module containing the application schemas.
    """

    @api_controller(
        prefix_or_class=controller_prefix,
        auth=CustomJWTAuth(),
        tags=[f"edit {model_name}"],
        permissions=[IsAuthenticated],
    )
    class CRUDController:
        Model = model

        @route.post(
            "",
            response={
                200: getattr(application_schemas, f"Get{model_name}ResponseSchema"),
                401: schemas.Http401UnauthorizedSchema,
            },
        )
        def create(
            self,
            request: WSGIRequest,
            body: getattr(application_schemas, f"Create{model_name}Schema"),  # type: ignore
        ) -> BaseModel:
            if isinstance(request.user, AnonymousUser):
                raise exceptions.Http401UnauthorizedException

            q = self.Model(**body.dict())

            try:
                q.create(request.user)
            except IntegrityError as e:
                raise exceptions.Http400BadRequestException("code already exists") from e

            return q

        @route.post(
            "/batch",
            response={
                200: list[getattr(application_schemas, f"Get{model_name}ResponseSchema")],
                401: schemas.Http401UnauthorizedSchema,
            },
        )
        def create_batch(
            self,
            request: WSGIRequest,
            body: list[getattr(application_schemas, f"Create{model_name}Schema")],  # type: ignore
        ) -> list[BaseModel]:
            if isinstance(request.user, AnonymousUser):
                raise exceptions.Http401UnauthorizedException

            try:
                with transaction.atomic():
                    created_objects = []

                    for item in body:
                        obj = self.Model(**item.dict())

                        obj.create(request.user)
                        created_objects.append(obj)

            except IntegrityError as e:
                raise exceptions.Http400BadRequestException(
                    "Batch operation failed: One or more records are invalid",
                ) from e
            except Exception as e:
                raise exceptions.Http400BadRequestException("Batch operation failed") from e

            return created_objects

        @route.get(
            "",
            response={
                200: list[getattr(application_schemas, f"Get{model_name}ResponseSchema")],
                401: schemas.Http401UnauthorizedSchema,
            },
        )
        def get_all(
            self,
            request: WSGIRequest,
        ) -> list[BaseModel]:
            if isinstance(request.user, AnonymousUser):
                raise exceptions.Http401UnauthorizedException

            return self.Model.objects.filter().values()  # type: ignore

        @route.get(
            "/{pk}",
            response={
                200: getattr(application_schemas, f"Get{model_name}ResponseSchema"),
                401: schemas.Http401UnauthorizedSchema,
                404: schemas.Http404NotFoundSchema,
            },
        )
        def get(self, request: WSGIRequest, pk: UUID) -> BaseModel:
            if isinstance(request.user, AnonymousUser):
                raise exceptions.Http401UnauthorizedException

            try:
                q = self.Model.objects.get(id=pk)
            except self.Model.DoesNotExist as e:
                raise exceptions.Http404NotFoundException from e

            if q.company_id != request.user.company_id:  # type: ignore
                raise exceptions.Http403ForbiddenException("You don't have permission to get this object.")

            return q

        @route.put(
            "/{pk}",
            response={
                200: schemas.BaseResponseSchema,
                401: schemas.Http401UnauthorizedSchema,
                404: schemas.Http404NotFoundSchema,
            },
        )
        def update(
            self,
            request: WSGIRequest,
            pk: UUID,
            body: getattr(application_schemas, f"Put{model_name}Schema"),  # type: ignore
        ) -> BaseModel:
            if isinstance(request.user, AnonymousUser):
                raise exceptions.Http401UnauthorizedException

            try:
                q = self.Model.objects.get(id=pk)
            except self.Model.DoesNotExist as e:
                raise exceptions.Http404NotFoundException from e

            for k, v in body.dict().items():
                setattr(q, k, v)

            try:
                q.save(request.user)
            except IntegrityError as e:
                raise exceptions.Http400BadRequestException("code already exists") from e

            return q

        @route.delete(
            "/{pk}",
            response={
                200: schemas.BaseResponseSchema,
                401: schemas.Http401UnauthorizedSchema,
                404: schemas.Http404NotFoundSchema,
            },
        )
        def delete(self, request: WSGIRequest, pk: UUID) -> dict:
            if isinstance(request.user, AnonymousUser):
                raise exceptions.Http401UnauthorizedException

            company_id = request.user.company_id  # type: ignore

            try:
                q = self.Model.objects.get(id=pk)
            except self.Model.DoesNotExist as e:
                raise exceptions.Http404NotFoundException from e

            if q.company_id != company_id:  # type: ignore
                raise exceptions.Http403ForbiddenException("You don't have permission to delete this object.")

            q.delete(request.user)

            return {"msg": "success"}

    return CRUDController


BASE_EXCLUDE_FIELD = [
    "created_at",
    "created_by_user",
    "updated_at",
    "updated_by_user",
    "is_delete",
    "deleted_at",
    "deleted_by_user",
]


BASE_GET_EXCLUDE_FIELD = BASE_EXCLUDE_FIELD

BASE_UPDATE_EXCLUDE_FIELD = [*BASE_EXCLUDE_FIELD, "id"]

BASE_CREATE_EXCLUDE_FIELD = [*BASE_EXCLUDE_FIELD, "id"]
