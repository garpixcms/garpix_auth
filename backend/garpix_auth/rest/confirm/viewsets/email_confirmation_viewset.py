from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.models import EmailConfirm
from garpix_auth.rest.confirm.permissions import NotAuthenticated
from garpix_auth.rest.confirm.serializers.email_confirmation_serializer import (EmailConfirmSendSerializer,
                                                                                EmailConfirmCheckCodeSerializer,
                                                                                EmailPreConfirmCheckCodeSerializer,
                                                                                EmailPreConfirmCheckSerializer,
                                                                                EmailPreConfirmSendSerializer)

User = get_user_model()


class EmailConfirmationViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = EmailConfirmSendSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = request.data('email', None)
            result = user.send_confirmation_code(email)
        else:
            serializer = EmailPreConfirmSendSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = EmailConfirm().send_confirmation_code(serializer.data['email'])
        return Response(result)

    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = EmailConfirmCheckCodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = user.check_confirmation_code(serializer.data['email_confirmation_code'])
        else:
            serializer = EmailPreConfirmCheckCodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = EmailConfirm().check_confirmation_code(serializer.data['email'],
                                                            serializer.data['email_confirmation_code'])
        return Response(result)

    @action(methods=["POST"], detail=False, permission_classes=(NotAuthenticated,))
    def check_confirmation(self, request, *args, **kwargs):
        serializer = EmailPreConfirmCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = EmailConfirm().check_confirmation(serializer.data['email'], serializer.data['token'])
        return Response(result)
