from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.models.confirm import PhoneConfirm
from garpix_auth.rest.confirm.permissions import NotAuthenticated
from garpix_auth.rest.confirm.serializers.phone_confirmation_serializer import (PhoneConfirmSendSerializer,
                                                                                PhoneConfirmCheckCodeSerializer,
                                                                                PhonePreConfirmCheckCodeSerializer,
                                                                                PhonePreConfirmCheckSerializer,
                                                                                PhonePreConfirmSendSerializer)

User = get_user_model()


class PhoneConfirmationViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = PhoneConfirmSendSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone = request.data('phone', None)
            result = user.send_confirmation_code(phone)
        else:
            serializer = PhonePreConfirmSendSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = PhoneConfirm().send_confirmation_code(serializer.data['phone'])
        return Response(result)

    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = PhoneConfirmCheckCodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = user.check_confirmation_code(serializer.data['phone_confirmation_code'])
        else:
            serializer = PhonePreConfirmCheckCodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = PhoneConfirm().check_confirmation_code(serializer.data['phone'],
                                                            serializer.data['phone_confirmation_code'])
        return Response(result)

    @action(methods=["POST"], detail=False, permission_classes=(NotAuthenticated,))
    def check_confirmation(self, request, *args, **kwargs):
        serializer = PhonePreConfirmCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = PhoneConfirm().check_confirmation(serializer.data['phone'], serializer.data['token'])
        return Response(result)
