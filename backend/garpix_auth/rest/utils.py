def get_token_from_request(request, keyword='Bearer'):
    if 'HTTP_AUTHORIZATION' not in request.META:
        return None

    token = request.META['HTTP_AUTHORIZATION']
    token = token[len(keyword) + 1:]
    return token
