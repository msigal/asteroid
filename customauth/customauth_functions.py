from typing import Dict

from customauth.models import CustomUser


def add_customuser(customuser_data: Dict[str, str]) -> CustomUser:
    return CustomUser.objects.create_user(
        email=customuser_data['email'],
        password=customuser_data['password1'],
    )
