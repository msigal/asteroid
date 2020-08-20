from django.urls import path

from api.views import (
    AsteroidViewSet,
    SignInView,
    SignUpView,
    UploadImageView,
)

urlpatterns = [
    path('signin/', SignInView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('asteroids/<str:name>/', AsteroidViewSet.as_view({'get': 'get_by_name'})),
    path('asteroids/<str:name>/bookmark/', AsteroidViewSet.as_view({'post': 'set_bookmark'})),
    path('upload-images/', UploadImageView.as_view()),
]
