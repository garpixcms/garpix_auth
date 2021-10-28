from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class PhoneConfirmSendSerializer(serializers.Serializer):
    phone = PhoneNumberField()


class PhoneConfirmCheckCodeSerializer(serializers.Serializer):
    phone_confirmation_code = serializers.models.CharField(max_length=15)


class PhonePreConfirmSendSerializer(serializers.Serializer):
    phone = PhoneNumberField()


class PhonePreConfirmCheckCodeSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    phone_confirmation_code = serializers.models.CharField(max_length=15)


class PhonePreConfirmCheckSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    token = serializers.models.CharField(max_length=40)
