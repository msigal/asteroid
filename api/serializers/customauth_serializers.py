from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        help_text='Email',
    )
    password1 = serializers.CharField(
        required=True,
        max_length=50,
        help_text='Пароль',
    )
    password2 = serializers.CharField(
        required=True,
        max_length=50,
        help_text='Повторите пароль',
    )

    def validate_password1(self, password1: str):
        if password1 != self.initial_data['password2']:
            raise serializers.ValidationError('password1 and password2 are not equal')
        return password1


class SignInSerializer(serializers.Serializer):
    # Copy Past AuthTokenSerializer, following changes:
    # - Username -> email
    # - lowercase(email)
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'), username=email,
                password=password
            )
        else:
            raise serializers.ValidationError(
                'Credentials are not provided'
            )

        attrs['user'] = user
        return attrs
