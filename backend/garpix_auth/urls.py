from django.urls import path
from rest_framework import routers

from garpix_auth.rest.obtain_auth_token import obtain_auth_token
from garpix_auth.rest.refresh_token_view import refresh_token_view
from garpix_auth.rest.logout_view import logout_view

from garpix_auth.rest.confirm.viewsets import EmailConfirmationViewSet, PhoneConfirmationViewSet
from garpix_auth.rest.restore_password.restore_password_viewset import RestorePasswordViewSet

urlpatterns = [
    path('login/', obtain_auth_token, name='api_login'),
    path('refresh/', refresh_token_view, name='api_refresh'),
    path('logout/', logout_view, name='api_logout'),
]

router = routers.DefaultRouter()
router.register(r'confirm_email', EmailConfirmationViewSet, basename='api_confirm_email')
router.register(r'confirm_phone', PhoneConfirmationViewSet, basename='api_confirm_phone')
router.register(r'restore_password', RestorePasswordViewSet, basename='api_restore_password')
urlpatterns += router.urls
