from drf_yasg import openapi

AUTHORIZATION_PARAM = openapi.Parameter(
    'authorization',
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    required=True,
    description='Токен подтверждающий авторизацию в системе',
)
