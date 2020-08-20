from django.contrib import admin
from django.contrib.auth.models import Group

from customauth.models import CustomUser

admin.site.register(CustomUser)
admin.site.unregister(Group)
