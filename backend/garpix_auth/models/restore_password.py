from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from garpix_notify.models import Notify
from garpix_utils.string import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
import string
from datetime import datetime, timezone


class RestorePasswordMixin(models.Model):

    phone = PhoneNumberField(verbose_name=_('Телефон'), max_length=30, blank=True, default='', unique=True)
    restore_password_confirm_code_phone = models.CharField(
        max_length=15, verbose_name='Код сброса пароля по телефону', null=True, blank=True)

    restore_password_confirm_code_email = models.CharField(
        max_length=15, verbose_name='Код сброса пароля по почте', null=True, blank=True)

    new_password = models.CharField(max_length=128, blank=True, null=True, verbose_name="Новый пароль")

    class Meta:
        abstract = True

    @classmethod
    def send_restore_code(cls, restore_value, code_type='email'):

        confirmation_code = get_random_string(settings.GARPIX_CONFIRM_CODE_LENGTH, string.digits)

        if code_type == 'email':

            user = cls.objects.filter(email=restore_value).first()
            if not user:
                return {"result": False, "message": "User with such email doesn't exist"}

            user.restore_password_confirm_code_email = confirmation_code
            user.save()

            Notify.send(settings.EMAIL_RESTORE_PASSWORD_EVENT, {
                'confirmation_code': confirmation_code
            }, email=user.email)

        else:

            user = cls.objects.filter(phone=restore_value).first()
            if not user:
                return {"result": False, "message": "User with such phone number doesn't exist"}
            user.restore_password_confirm_code_phone = confirmation_code
            user.save()

            Notify.send(settings.PHONE_RESTORE_PASSWORD_EVENT, {
                'confirmation_code': confirmation_code
            }, phone=user.phone)

        return {"result": True}

    @classmethod
    def set_new_password(cls, restore_value, confirmation_code, new_password, code_type='email'):

        if code_type == 'email':

            user = cls.objects.filter(email=restore_value, restore_password_confirm_code_email=confirmation_code).first()
            if not user:
                return {"result": False, "message": "Email or code is incorrect"}

            time_is_up = (datetime.now(
                timezone.utc) - user.updated_at).days > settings.GARPIX_CONFIRM_EMAIL_CODE_LIFE_TIME

            if time_is_up:
                return {"result": False, "message": "Code has expired"}

        else:
            user = cls.objects.filter(phone=restore_value, restore_password_confirm_code_phone=confirmation_code).first()
            if not user:
                return {"result": False, "message": "Phone number or code is incorrect"}

            time_is_up = (datetime.now(
                timezone.utc) - user.updated_at).seconds / 60 > settings.GARPIX_CONFIRM_PHONE_CODE_LIFE_TIME

            if time_is_up:
                return {"result": False, "message": "Code has expired"}

        user.set_password(new_password)
        user.new_password = ''  # чтоб не хранить в открытом виде пароль
        user.save()

        return {"result": True, "message": "password was successfully updated"}
