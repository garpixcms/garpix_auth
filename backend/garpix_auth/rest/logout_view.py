from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from oauth2_provider.models import AccessToken
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.refresh_token import RefreshToken
from rest_framework.permissions import IsAuthenticated


class LogoutView(APIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            AccessToken.objects.filter(user=request.user).delete()
            RefreshToken.objects.filter(user=request.user).delete()
            return Response({
                'result': True,
            })
        return Response({
            'result': False,
        }, status=401)


logout_view = LogoutView.as_view()
