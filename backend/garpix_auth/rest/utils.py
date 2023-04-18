from django.conf import settings


def get_token_from_request(request, keyword='Bearer'):
    header_key = getattr(settings, 'GARPIX_REST_AUTH_HEADER_KEY', 'HTTP_AUTHORIZATION')
    if header_key not in request.META:
        return None
    token = request.META[header_key]
    token = token[len(keyword) + 1:]
    return token
