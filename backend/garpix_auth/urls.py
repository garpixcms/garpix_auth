from django.urls import path
from garpix_auth.rest.obtain_auth_token import obtain_auth_token
from garpix_auth.rest.refresh_token_view import refresh_token_view
from garpix_auth.rest.logout_view import logout_view

urlpatterns = [
    path('login/', obtain_auth_token, name='api_login'),
    path('refresh/', refresh_token_view, name='api_refresh'),
    path('logout/', logout_view, name='api_logout'),
]
