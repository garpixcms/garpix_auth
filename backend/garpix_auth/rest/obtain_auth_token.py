from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from .auth_token_serializer import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from ..models.refresh_token import RefreshToken
from datetime import timedelta
from django.utils import timezone


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        refresh_token, created_refresh_token = RefreshToken.objects.get_or_create(user=user)
        if not created:
            if settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS > 0:
                if token.created + timedelta(seconds=settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS) < timezone.now():
                    token.delete()
                    token, created = Token.objects.get_or_create(user=user)
                    if not created_refresh_token:
                        RefreshToken.objects.filter(user=user).delete()
                        refresh_token, created_refresh_token = RefreshToken.objects.get_or_create(user=user)
        return Response({
            'access_token': token.key,
            'refresh_token': refresh_token.key,
            'token_type': 'Bearer',
            'access_token_expires': settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS,
            'refresh_token_expires': settings.GARPIX_REFRESH_TOKEN_TTL_SECONDS,
        })


obtain_auth_token = ObtainAuthToken.as_view()
