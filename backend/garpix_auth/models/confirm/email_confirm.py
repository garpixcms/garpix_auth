from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from garpix_notify.models import Notify
from garpix_utils.string import get_random_string
import string
from django.core.exceptions import ValidationError
from rest_framework import serializers

from uuid import uuid4

User = get_user_model()


class UserEmailConfirmMixin(models.Model):
    """
    Миксин для подтверждения email после регистрации
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    is_email_confirmed = models.BooleanField(default=False, verbose_name="Email подтвержден")
    email_confirmation_code = models.CharField(max_length=15, verbose_name='Код подтверждения email',
                                               blank=True, default='')
    new_email = models.EmailField(unique=True, blank=True, default='', verbose_name="Новый email")

    def send_confirmation_code(self, email=None):

        if not email:
            email = self.email

        anybody_have_this_email = User.objects.filter(email=email, is_email_confirmed=True).count() > 0

        if not anybody_have_this_email.exists() or anybody_have_this_email == self:
            confirmation_code = get_random_string(settings.GARPIX_CONFIRM_CODE_LENGTH, string.digits)

            self.new_email = email
            self.email_confirmation_code = confirmation_code

            Notify.send(settings.EMAIL_CONFIRMATION_EVENT, {
                'confirmation_code': confirmation_code
            }, email=email)

            return {"result": True}

        return {"result": False, "message": "User with such email already exists"}

    def check_confirmation_code(self, email_confirmation_code):

        time_is_up = (datetime.now(
            timezone.utc) - self.updated_at).days > settings.GARPIX_CONFIRM_EMAIL_CODE_LIFE_TIME

        if time_is_up:
            return {"result": False, "message": "Code has expired"}

        if self.email_confirmation_code != email_confirmation_code:
            return {"result": False, "message": "Code is incorrect"}

        self.is_email_confirmed = True
        self.email = self.new_email
        self.save()
        return {"result": True}

    class Meta:
        abstract = True


class EmailConfirm(models.Model):
    """
    Модель для подтверждения email до регистрации
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    is_email_confirmed = models.BooleanField(default=False, verbose_name="Email подтвержден")
    email_confirmation_code = models.CharField(max_length=255, verbose_name="Код подтверждения email")
    token = models.CharField(max_length=40, verbose_name="Токен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    @classmethod
    def send_confirmation_code(cls, email):

        anybody_have_this_email = User.objects.filter(email=email, is_email_confirmed=True).count() > 0
        if not anybody_have_this_email:
            email_confirmation_instance = cls.objects.filter(email=email).first() or cls(
                email=email)

            confirmation_code = get_random_string(settings.GARPIX_CONFIRM_CODE_LENGTH, string.digits)
            email_confirmation_instance.email_confirmation_code = confirmation_code
            email_confirmation_instance.token = uuid4()

            try:
                email_confirmation_instance.full_clean()
            except ValidationError as e:
                return serializers.ValidationError(e)

            email_confirmation_instance.save()

            Notify.send(settings.EMAIL_CONFIRMATION_EVENT, {
                'confirmation_code': confirmation_code
            }, email=email)

            return {"result": True}

        return {"result": False, "message": "User with such email already exists"}

    @classmethod
    def check_confirmation_code(cls, email, email_confirmation_code):
        email_confirmation_instance = cls.objects.filter(email=email,
                                                         email_confirmation_code=email_confirmation_code).first()

        if not email_confirmation_instance:
            return {"result": False, "message": "Code or email is incorrect"}

        time_is_up = (datetime.now(
            timezone.utc) - email_confirmation_instance.updated_at).seconds / 60 > settings.GARPIX_CONFIRM_EMAIL_CODE_LIFE_TIME

        if time_is_up:
            return {"result": False, "message": "Code has expired"}
        email_confirmation_instance.is_email_confirmed = True
        email_confirmation_instance.save()
        return {"token": email_confirmation_instance.token, "result": True}

    @classmethod
    def check_confirmation(cls, email, token):
        """
         метод проверяет, подтвержден ли email пользователем
         """
        if cls.objects.filter(email=email, is_email_confirmed=True, token=token).first():
            return {"result": True}
        return {"result": False}

    class Meta:
        verbose_name = 'Код подтверждения по email'
        verbose_name_plural = 'Коды подтверждения по email'
