from django.conf import settings

from .backend import CustomAuthenticationBackend  # noqa
from .refresh_token import RefreshToken  # noqa
from .access_token import AccessToken  # noqa

from .confirm import UserEmailConfirmMixin, UserPhoneConfirmMixin

from .restore_password import RestorePasswordMixin

if settings.GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION:
    from .confirm import PhoneConfirm  # noqa

if settings.GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION:
    from .confirm import EmailConfirm  # noqa
