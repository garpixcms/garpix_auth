AUTHENTICATION_BACKENDS = (
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

PHONE_CONFIRMATION_EVENT = 2021
EMAIL_CONFIRMATION_EVENT = 2022
EMAIL_CONFIRMATION_BY_LINK_EVENT = 2023

PHONE_CONFIRMATION_EVENT_ITEM = {
    PHONE_CONFIRMATION_EVENT: {
        'title': 'Подтверждение номера телефона',
        'context_description': '{{ confirmation_code }}'
    }
}

EMAIL_CONFIRMATION_EVENT_ITEM = {
    EMAIL_CONFIRMATION_EVENT: {
        'title': 'Подтверждение email',
        'context_description': '{{ confirmation_code }}'
    }
}

EMAIL_CONFIRMATION__BY_LINK_EVENT_ITEM = {
    EMAIL_CONFIRMATION_BY_LINK_EVENT: {
        'title': 'Подтверждение email по ссылке',
        'context_description': '{{ link }}'
    }
}


GARPIX_CONFIRM_CODE_LENGTH = 6
GARPIX_CONFIRM_PHONE_CODE_LIFE_TIME = 5  # in minutes
GARPIX_CONFIRM_EMAIL_CODE_LIFE_TIME = 2  # in days

GARPIX_CONFIRM_EMAIL_LINK_LENGTH = 64

GARPIX_USE_PREREGISTRATION_PHONE_CONFIRMATION = True

GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION = True

NOTIFY_EVENTS = {}

NOTIFY_EVENTS.update(PHONE_CONFIRMATION_EVENT_ITEM)
NOTIFY_EVENTS.update(EMAIL_CONFIRMATION_EVENT_ITEM)

CHOICES_NOTIFY_EVENT = [(k, v['title']) for k, v in NOTIFY_EVENTS.items()]
