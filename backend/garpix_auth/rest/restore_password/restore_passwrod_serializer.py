from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

CODE_TYPES = [
    ('EMAIL', 'Email'),
    ('PHONE', 'Phone')
]


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class RestoreCommonSerializer(serializers.Serializer):
    code_type = ChoiceField(choices=CODE_TYPES)


class RestoreByEmailSerializer(serializers.Serializer):
    restore_value = serializers.EmailField(required=True)


class RestoreByPhoneSerializer(serializers.Serializer):
    restore_value = PhoneNumberField(required=True)


class RestoreSetPasswordByEmailSerializer(serializers.Serializer):
    restore_value = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(max_length=15, required=True)
    new_password = serializers.CharField(max_length=255, required=True)


class RestoreSetPasswordByPhoneSerializer(serializers.Serializer):
    restore_value = PhoneNumberField(required=True)
    confirmation_code = serializers.CharField(max_length=15, required=True)
    new_password = serializers.CharField(max_length=255, required=True)
