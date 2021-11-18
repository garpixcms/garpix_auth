from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from garpix_notify.models import Notify
from garpix_utils.string import get_random_string
import string
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import serializers

from uuid import uuid4

User = get_user_model()


CONFIRM_CODE_LENGTH = settings.GARPIX_CONFIRM_CODE_LENGTH if hasattr(settings,
                                                                     'GARPIX_CONFIRM_CODE_LENGTH') else 6

CONFIRM_PHONE_CODE_LIFE_TIME = settings.GARPIX_CONFIRM_PHONE_CODE_LIFE_TIME if hasattr(settings,
                                                                                       'GARPIX_CONFIRM_PHONE_CODE_LIFE_TIME') else 6


class UserPhoneConfirmMixin(models.Model):
    """
    Миксин для подтверждения номера телефона после регистрации
    """
    phone = PhoneNumberField(unique=True, blank=True, default='', verbose_name="Номер телефона")
    is_phone_confirmed = models.BooleanField(default=False, verbose_name="Номер телефона подтвержден")
    phone_confirmation_code = models.CharField(max_length=15, verbose_name='Код подтверждения номера телефона',
                                               blank=True, null=True)
    new_phone = PhoneNumberField(unique=True, blank=True, null=True, verbose_name="Новый номер телефона")

    def send_phone_confirmation_code(self, phone=None):
        if not phone:
            phone = self.phone

        anybody_have_this_phone = User.objects.filter(phone=phone, is_phone_confirmed=True).first()

        if not anybody_have_this_phone.exists() or anybody_have_this_phone == self:
            confirmation_code = get_random_string(CONFIRM_CODE_LENGTH, string.digits)
            self.new_phone = phone
            self.phone_confirmation_code = confirmation_code
            self.save()
            Notify.send(settings.PHONE_CONFIRMATION_EVENT, {
                'confirmation_code': confirmation_code
            }, phone=phone)
            return {"result": True}

        return {"result": False, "message": "User with such phone number already exists"}

    def check_phone_confirmation_code(self, phone_confirmation_code):

        time_is_up = (datetime.now(
            timezone.utc) - self.updated_at).seconds / 60 > CONFIRM_PHONE_CODE_LIFE_TIME

        if time_is_up:
            return {"result": False, "message": "Code has expired"}

        if self.phone_confirmation_code != phone_confirmation_code:
            return {"result": False, "message": "Code is incorrect"}

        self.is_phone_confirmed = True
        self.phone = self.new_phone
        self.save()
        return True

    class Meta:
        abstract = True


class PhoneConfirm(models.Model):
    """
    Модель для подтверждения номера телефона до регистрации
    """
    phone = PhoneNumberField(unique=True, verbose_name="Телефон")
    is_phone_confirmed = models.BooleanField(default=False, verbose_name="Номер телефона подтвержден")
    phone_confirmation_code = models.CharField(max_length=15, verbose_name='Код подтверждения номера телефона')
    token = models.CharField(max_length=40, verbose_name="Токен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    @classmethod
    def send_confirmation_code(cls, phone):

        anybody_have_this_phone = User.objects.filter(phone=phone, is_phone_confirmed=True).count() > 0
        if not anybody_have_this_phone:
            phone_confirmation_instance = cls.objects.filter(phone=phone).first() or cls(phone=phone)

            confirmation_code = get_random_string(CONFIRM_CODE_LENGTH, string.digits)
            phone_confirmation_instance.phone_confirmation_code = confirmation_code
            phone_confirmation_instance.token = uuid4()

            try:
                phone_confirmation_instance.full_clean()
            except ValidationError as e:
                return serializers.ValidationError(e)

            phone_confirmation_instance.save()

            Notify.send(settings.PHONE_CONFIRMATION_EVENT, {
                'confirmation_code': confirmation_code
            }, phone=phone)

            return {"result": True}

        return {"result": False, "message": "User with such phone number already exists"}

    @classmethod
    def check_confirmation_code(cls, phone, phone_confirmation_code):
        phone_confirmation_instance = cls.objects.filter(phone=phone,
                                                         phone_confirmation_code=phone_confirmation_code).first()

        if not phone_confirmation_instance:
            return {"result": False, "message": "Code or phone number is incorrect"}

        time_is_up = (datetime.now(
            timezone.utc) - phone_confirmation_instance.updated_at).seconds / 60 > CONFIRM_PHONE_CODE_LIFE_TIME

        if time_is_up:
            return {"result": False, "message": "Code has expired"}

        phone_confirmation_instance.is_phone_confirmed = True
        phone_confirmation_instance.save()
        return {"token": phone_confirmation_instance.token, "result": True}

    @classmethod
    def check_confirmation(cls, phone, token):
        """
         метод проверяет, подтвержден ли номер телефона пользователем
         """
        if cls.objects.filter(phone=phone, is_phone_confirmed=True, token=token).first():
            return True
        return False

    class Meta:
        verbose_name = 'Код подтверждения по смс'
        verbose_name_plural = 'Коды подтверждения по смс'
        if not hasattr(settings,
                       'GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION') or not settings.GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION:
            abstract = True
