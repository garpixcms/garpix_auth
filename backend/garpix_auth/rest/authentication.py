from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model


def get_user_by_token(token):
    from rest_framework.authtoken.models import Token
    from oauth2_provider.models import AccessToken
    User = get_user_model()

    try:
        tok = Token.objects.get(key=token)
        user = User.objects.get(id=tok.user_id)
        return user
    except: # noqa
        pass

    try:
        user = AccessToken.objects.get(token=token).user
        return user
    except: # noqa
        pass

    return None


class MainAuthentication(TokenAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        from rest_framework.authtoken.models import Token
        from oauth2_provider.models import AccessToken
        User = get_user_model()

        if 'HTTP_AUTHORIZATION' not in request.META:
            return None

        token = request.META['HTTP_AUTHORIZATION']
        token = token[len(self.keyword) + 1:]

        # Django auth-token
        try:
            tok = Token.objects.get(key=token)
            user = User.objects.get(id=tok.user_id)
            return user, None

        except: # noqa
            pass

        # social auth by means of DRSA2
        try:
            user = AccessToken.objects.get(token=token).user

            return user, None

        except: # noqa
            return None
