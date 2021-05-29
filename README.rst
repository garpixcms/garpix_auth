
Garpix Auth
===========

Auth module for Django/DRF projects. Part of GarpixCMS.

Used packages: 


* `django rest framework <https://www.django-rest-framework.org/api-guide/authentication/>`_
* `social-auth-app-django <https://github.com/python-social-auth/social-app-django>`_
* `django-rest-framework-social-oauth2 <https://github.com/RealmTeam/django-rest-framework-social-oauth2>`_
* etc; see setup.py

Quickstart
----------

Install with pip:

.. code-block:: bash

   pip install garpix_auth

Add the ``garpix_auth`` to your ``INSTALLED_APPS``\ :

.. code-block:: python

   # settings.py

   INSTALLED_APPS = [
       # ...
       'garpix_auth',
   ]

Add to ``urls.py``\ :

.. code-block::

   from garpix_auth.views import LogoutView, LoginView

   urlpatterns = [
       # ...
       path('logout/', LogoutView.as_view(url='/'), name="logout"),
       path('login/', LoginView.as_view(), name="authorize"),
       # ...
   ]

For custom auth with phone and email use this in ``settings.py``\ :

.. code-block::

   AUTHENTICATION_BACKENDS = (
       # Django
       'garpix_auth.models.CustomAuthenticationBackend',
       'django.contrib.auth.backends.ModelBackend',
   )

With Django Rest Framework
--------------------------

Add this for SPA:

.. code-block::

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

Add to ``urls.py``\ :

.. code-block::

   from garpix_auth.rest.obtain_auth_token import obtain_auth_token

   urlpatterns = [
       # ...
       path('token-auth/', obtain_auth_token),
       # ...
   ]

Changelog
=========

See `CHANGELOG.md <CHANGELOG.md>`_.

Contributing
============

See `CONTRIBUTING.md <CONTRIBUTING.md>`_.

License
=======

`MIT <LICENSE>`_

----

Developed by Garpix / `https://garpix.com <https://garpix.com>`_
