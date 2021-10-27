from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.models import EmailConfirm
from garpix_auth.rest.confirm.permissions import NotAuthenticated

User = get_user_model()


class EmailConfirmationViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        user = request.user
        if authenticate(user) is not None:
            result = user.send_confirmation_code(email)
        else:
            result = EmailConfirm().send_confirmation_code(email)
        return Response(result)

    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        confirm_code = request.data.get('email_confirmation_code', None)
        user = request.user
        if authenticate(user) is not None:
            result = user.check_confirmation_code(confirm_code)
        else:
            result = EmailConfirm().check_confirmation_code(email, confirm_code)
        return Response(result)

    @action(methods=["POST"], detail=False, permission_classes=(NotAuthenticated,))
    def check_confirmation(self, request, *args, **kwargs):
        token = request.data.get('token')
        email = request.data.get('email')
        result = EmailConfirm().check_confirmation(email, token)
        return Response(result)
