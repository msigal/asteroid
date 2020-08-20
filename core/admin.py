from django.contrib import admin

from core.models import (
    Asteroid,
    BookmarkAsteroid,
    UploadedImage,

)

admin.site.register(Asteroid)
admin.site.register(BookmarkAsteroid)
admin.site.register(UploadedImage)
