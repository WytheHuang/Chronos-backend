import io
import json
import re
import zipfile
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any
from uuid import UUID

import django.utils.timezone as django_timezone
from core import exceptions as core_exceptions
from core import schemas as core_schemas
from core import utils as core_utils
from core.apis import BaseEditApiController
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import CharField
from django.db.models import F
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django_celery_results.models import TaskResult
from ninja_extra import api_controller
from ninja_extra import route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from . import models
from . import schemas
from . import utils


@api_controller(
    prefix_or_class="chatbot",
    auth=JWTAuth(),
    tags=["chatbot"],
    permissions=[IsAuthenticated],
)
class ChatbotApiController(BaseEditApiController):
    @route.get("/test")
    def test(self, request: WSGIRequest) -> Any:
        return {"message": "Hello World!"}
