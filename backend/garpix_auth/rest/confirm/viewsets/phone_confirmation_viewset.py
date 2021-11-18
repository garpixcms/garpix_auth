from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.models.confirm import PhoneConfirm
from garpix_auth.rest.confirm.serializers.phone_confirmation_serializer import (PhoneConfirmSendSerializer,
                                                                                PhoneConfirmCheckCodeSerializer,
                                                                                PhonePreConfirmCheckCodeSerializer,
                                                                                PhonePreConfirmSendSerializer)

User = get_user_model()


class PhoneConfirmationViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return PhoneConfirmSendSerializer
        return PhonePreConfirmCheckCodeSerializer

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = PhoneConfirmSendSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone = request.data('phone', None)
            result = user.send_phone_confirmation_code(phone)
        else:
            if hasattr(settings,
                       'GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION') and settings.GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION:
                serializer = PhonePreConfirmSendSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = PhoneConfirm().send_confirmation_code(serializer.data['phone'])
            else:
                return Response({'Учетные данные не были предоставлены'}, status=401)
        return Response(result)

    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = PhoneConfirmCheckCodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = user.check_phone_confirmation_code(serializer.data['phone_confirmation_code'])
        else:
            if hasattr(settings,
                       'GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION') and settings.GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION:
                serializer = PhonePreConfirmCheckCodeSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = PhoneConfirm().check_confirmation_code(serializer.data['phone'],
                                                                serializer.data['phone_confirmation_code'])
            else:
                return Response({'Учетные данные не были предоставлены'}, status=401)
        return Response(result)
