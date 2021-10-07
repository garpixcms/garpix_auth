from django.contrib.auth import get_user_model
from django.db.models import Q


class CustomAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = get_user_model().objects.get(Q(phone=username) | Q(username=username.lower()))
            pwd_valid = user.check_password(password)
            if pwd_valid:
                return user
            return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
