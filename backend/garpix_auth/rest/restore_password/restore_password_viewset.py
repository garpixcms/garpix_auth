from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.rest.restore_password.restore_passwrod_serializer import (RestoreCommonSerializer,
                                                                           RestoreByEmailSerializer,
                                                                           RestoreByPhoneSerializer,
                                                                           RestoreSetPasswordByEmailSerializer,
                                                                           RestoreSetPasswordByPhoneSerializer)

User = get_user_model()


class RestorePasswordViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    def restore_password(self, request, *args, **kwargs):
        common_serializer = RestoreCommonSerializer(data=request.data)
        common_serializer.is_valid(raise_exception=True)

        if common_serializer.data['code_type'] == 'email':
            value_serializer = RestoreByEmailSerializer(data=request.data)
            value_serializer.is_valid(raise_exception=True)
        else:
            value_serializer = RestoreByPhoneSerializer(data=request.data)
            value_serializer.is_valid(raise_exception=True)

        result = User().send_restore_code(restore_value=value_serializer.data['restore_value'],
                                          code_type=common_serializer.data['code_type'])

        return Response(result)

    @action(methods=['POST'], detail=False)
    def set_password(self, request, *args, **kwargs):
        common_serializer = RestoreCommonSerializer(data=request.data)
        common_serializer.is_valid(raise_exception=True)

        if common_serializer.data['code_type'] == 'email':
            value_serializer = RestoreSetPasswordByEmailSerializer(data=request.data)
            value_serializer.is_valid(raise_exception=True)
        else:
            value_serializer = RestoreSetPasswordByPhoneSerializer(data=request.data)
            value_serializer.is_valid(raise_exception=True)

        result = User().set_new_password(restore_value=value_serializer.data['restore_value'],
                                         confirmation_code=value_serializer.data['confirmation_code'],
                                         new_password=value_serializer.data['new_password'],
                                         code_type=common_serializer.data['code_type'])

        return Response(result)
