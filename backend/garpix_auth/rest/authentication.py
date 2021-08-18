from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


def get_user_by_token(token):
    from rest_framework.authtoken.models import Token
    from oauth2_provider.models import AccessToken
    User = get_user_model()

    # Refresh django rest token
    try:
        tok = Token.objects.get(key=token)
        if settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS > 0:
            if tok.created + timedelta(seconds=settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS) < timezone.now():
                tok.delete()
                raise Exception("Token expired.")
        user = User.objects.get(id=tok.user_id)
        return user
    except: # noqa
        pass

    # Refresh social auth token
    try:
        tok = AccessToken.objects.get(token=token)
        if settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS > 0:
            if tok.created + timedelta(seconds=settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS) < timezone.now():
                tok.delete()
        else:
            user = tok.user
            return user
    except: # noqa
        pass

    return None


class MainAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return None

        token = request.META['HTTP_AUTHORIZATION']
        token = token[len(self.keyword) + 1:]

        user = get_user_by_token(token)
        if user is not None:
            return user, None
        return None
