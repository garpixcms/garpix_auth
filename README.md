# Garpix Auth

Auth module for Django/DRF projects. Part of GarpixCMS.

Used packages: 

* [django rest framework](https://www.django-rest-framework.org/api-guide/authentication/)
* [social-auth-app-django](https://github.com/python-social-auth/social-app-django)
* [django-rest-framework-social-oauth2](https://github.com/RealmTeam/django-rest-framework-social-oauth2)
* etc; see setup.py

## Quickstart

Install with pip:

```bash
pip install garpix_auth
```

Add the `garpix_auth` to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'garpix_auth',
]
```

Add to `urls.py`:

```
from garpix_auth.views import LogoutView, LoginView

urlpatterns = [
    # ...
    path('logout/', LogoutView.as_view(url='/'), name="logout"),
    path('login/', LoginView.as_view(), name="authorize"),
    # ...
]
```

For custom auth with phone and email use this in `settings.py`:

```
AUTHENTICATION_BACKENDS = (
    # Django
    'garpix_auth.models.CustomAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)
```

## With Django Rest Framework

Add this for SPA:

```
INSTALLED_APPS += [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': {
        'garpix_auth.rest.authentication.MainAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    }
}

AUTHENTICATION_BACKENDS = (
    # Only your social networks
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Django
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

```

Add to `urls.py`:

```
from django.urls import path, include

urlpatterns = [
    # ...
    path('api/auth/', include(('garpix_auth.urls', 'garpix_auth'), namespace='garpix_auth')),
    # ...
]
```

See `garpix_auth/tests/test_api.py` for examples.


To use email and phone confirmation or (and) restore password functionality add the `garpix_notify` to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'garpix_notify',
]
```
and to migration modules:

```python
# settings.py

MIGRATION_MODULES = {
    'garpix_notify': 'app.migrations.garpix_notify',
}
```

Add corresponding mixin(s) to your User model:
```python
from garpix_auth.models import UserEmailConfirmMixin, UserPhoneConfirmMixin, RestorePasswordMixin  # noqa
```

You also need import email or(and) phone confirmation notify events:
```python
from garpix_auth.settings import EMAIL_CONFIRMATION_EVENT, EMAIL_CONFIRMATION_EVENT_ITEM  # noqa
from garpix_auth.settings import PHONE_CONFIRMATION_EVENT, PHONE_CONFIRMATION_EVENT_ITEM  # noqa

NOTIFY_EVENTS = {}  #  if you haven't any notifications in your project

NOTIFY_EVENTS.update(PHONE_CONFIRMATION_EVENT_ITEM)
NOTIFY_EVENTS.update(EMAIL_CONFIRMATION_EVENT_ITEM)

```
The same notification events to restore password:
```python
from garpix_auth.settings import EMAIL_RESTORE_PASSWORD_EVENT, EMAIL_RESTORE_PASSWORD_EVENT_ITEM  # noqa
from garpix_auth.settings import PHONE_RESTORE_PASSWORD_EVENT, PHONE_RESTORE_PASSWORD_EVENT_ITEM  # noqa
NOTIFY_EVENTS = {}  #  if you haven't any notifications in your project

NOTIFY_EVENTS.update(PHONE_RESTORE_PASSWORD_EVENT_ITEM)
NOTIFY_EVENTS.update(EMAIL_RESTORE_PASSWORD_EVENT_ITEM)

```
You can specify email and phone code length and lifetime:
```python
GARPIX_CONFIRM_CODE_LENGTH = 6
GARPIX_CONFIRM_PHONE_CODE_LIFE_TIME = 5  # in minutes
GARPIX_CONFIRM_EMAIL_CODE_LIFE_TIME = 2  # in days
```

If you need to use pre-registration email or phone confirmation, you need to set corresponding variables to True:
```python
GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION = True

GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION = True
```

# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)