from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from .refresh_token_serializer import RefreshTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from ..models.refresh_token import RefreshToken
from django.utils import timezone
from datetime import timedelta


class RefreshTokenView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']
        try:
            refresh_token_obj = RefreshToken.objects.get(key=refresh_token)
            if settings.GARPIX_REFRESH_TOKEN_TTL_SECONDS > 0:
                if refresh_token_obj.created + timedelta(seconds=settings.GARPIX_REFRESH_TOKEN_TTL_SECONDS) < timezone.now():
                    refresh_token_obj.delete()
                    Token.objects.filter(user=refresh_token_obj.user).delete()
                    raise Exception("Token expired.")
            Token.objects.filter(user=refresh_token_obj.user).update(created=timezone.now())
            token, created = Token.objects.get_or_create(user=refresh_token_obj.user)
            return Response({
                'access_token': token.key,
                'access_token_expires': settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS,
                'result': True,
            })
        except:  # noqa
            return Response({'result': False})


refresh_token_view = RefreshTokenView.as_view()
