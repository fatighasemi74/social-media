from rest_framework.authentication import get_authorization_header
from rest_framework import authentication

def get_access_token(self, request):
    header = get_authorization_header(request)
    if not header:
        return None
    header = header.decode(authentication.HTTP_HEADER_ENCODING)

    auth = header.split()
    print(auth)