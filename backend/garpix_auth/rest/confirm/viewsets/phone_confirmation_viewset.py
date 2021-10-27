from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.rest.confirm.permissions import NotAuthenticated
from garpix_auth.models import PhoneConfirm

User = get_user_model()


class PhoneConfirmationViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        phone = request.data.get('phone', None)
        user = request.user
        if authenticate(user) is not None:
            result = user.send_confirmation_code(phone)
        else:
            result = PhoneConfirm().send_confirmation_code(phone)
        return Response(result)

    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        phone = request.data.get('phone', None)
        confirm_code = request.data.get('phone_confirmation_code', None)
        user = request.user
        if authenticate(user) is not None:
            result = user.check_confirmation_code(confirm_code)
        else:
            result = PhoneConfirm().check_confirmation_code(phone, confirm_code)
        return Response(result)

    @action(methods=["POST"], detail=False, permission_classes=(NotAuthenticated,))
    def check_confirmation(self, request, *args, **kwargs):
        token = request.data.get('token')
        phone = request.data.get('phone')
        result = PhoneConfirm().check_confirmation(phone, token)
        return Response(result)
