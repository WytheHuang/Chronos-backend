from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


if typing.TYPE_CHECKING:
    from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    """Adapter class for customizing account registration behavior.

    This class extends the DefaultAccountAdapter, providing custom logic to determine
    if new account signups are allowed based on application settings.
    """
    def is_open_for_signup(self: AccountAdapter, request: HttpRequest) -> bool:  # noqa: ARG002
        """Determines whether new account registrations are currently permitted.

        This method overrides the default signup check to allow or disallow user
        registration based on the application's configuration settings.

        Args:
            self (AccountAdapter): An instance of AccountAdapter.
            request (HttpRequest): The incoming HTTP request, typically from a user attempting to sign up.

        Returns:
            bool: True if signups are allowed according to the settings, False otherwise.
        """
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


# social account adapter
# class SocialAccountAdapter(DefaultSocialAccountAdapter):
#     def is_open_for_signup(self, request: HttpRequest, sociallogin: SocialLogin) -> bool:
#         return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

#     def populate_user(self, request: HttpRequest, sociallogin: SocialLogin, data: dict[str, typing.Any]) -> User:
#         """
#         Populates user information from social provider info.

#         See: https://django-allauth.readthedocs.io/en/latest/advanced.html?#creating-and-populating-user-instances
#         """
#         user = sociallogin.user
#         if name := data.get("name"):
#             user.name = name
#         elif first_name := data.get("first_name"):
#             user.name = first_name
#             if last_name := data.get("last_name"):
#                 user.name += f" {last_name}"
#         return super().populate_user(request, sociallogin, data)
