from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.exceptions import APIError
from api.serializers import (
    AsteroidDetailsSerializer,
    SignInSerializer,
    SignUpSerializer,
    SetBookmarkSerializer,
    UploadImageSerializer,
)
from api.swagger.params import AUTHORIZATION_PARAM
from api.utils import check_asteroid_exists
from core.core_functions import (
    add_uploaded_image_data,
    get_asteroid_by_name,
    get_uploaded_image_urls,
    set_asteroid_bookmark_status,
)
from customauth.customauth_functions import add_customuser
from rest_framework.parsers import FileUploadParser


class SignUpView(views.APIView):
    """ Api view for User registration"""

    @swagger_auto_schema(
        tags=['auth'],
        operation_id='api_signup',
        responses={
            201: 'User created successfully',
            400: 'Invalid Data',
        },
        request_body=SignUpSerializer,
    )
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.run_validation(data=request.data)
        try:
            user = add_customuser(data)
            return Response(
                {'message': f'User {user} successfully created'},
                status=status.HTTP_201_CREATED,
            )
        except APIError:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignInView(ObtainAuthToken):
    """Api view for User authorization / Returns Token"""
    serializer_class = SignInSerializer

    @swagger_auto_schema(
        tags=['auth'],
        operation_id='api_signin',
        responses={
            201: 'Authorization successfully',
            400: 'Invalid Data',
        },
        request_body=SignInSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AsteroidViewSet(viewsets.ViewSet):
    """Asteroid View Set"""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id='api_asteroid_get_by_name',
        tags=['asteroid'],
        manual_parameters=(AUTHORIZATION_PARAM,),
        responses={
            200: AsteroidDetailsSerializer,
            400: 'Bad request, please contact administrator',
            401: 'An attempt to request without successful authorization',
            404: 'Asteroid not found',
        }
    )
    @check_asteroid_exists
    def get_by_name(self, request, asteroid_name: str):
        """Get details by Asteroid Name"""
        asteroid_data = get_asteroid_by_name(asteroid_name).to_dict()
        asteroid_data['image_urls'] = get_uploaded_image_urls(user=request.user, asteroid_name=asteroid_name)
        serializer = AsteroidDetailsSerializer(data=asteroid_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id='api_asteroid_add_to_bookmarks',
        tags=['asteroid'],
        manual_parameters=(AUTHORIZATION_PARAM,),
        responses={
            200: 'Asteroid bookmark edited successfully for current user',
            400: 'Bad request, please contact administrator',
            401: 'An attempt to request without successful authorization',
            404: 'Asteroid not found',
        },
        request_body=SetBookmarkSerializer,
    )
    @check_asteroid_exists
    def set_bookmark(self, request, asteroid_name: str):
        """Add Asteroid to bookmarks for current user"""
        user = request.user
        serializer = SetBookmarkSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.run_validation(data=request.data)

        try:
            set_asteroid_bookmark_status(user, asteroid_name, data)
            return Response(
                {'message': f'Bookmark status for asteroid {asteroid_name} successfully updated'},
                status=status.HTTP_201_CREATED,
            )
        except APIError:
            return Response(
                {'error': APIError},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UploadImageView(views.APIView):
    """Api view for image upload"""
    parser_class = (FileUploadParser,)

    @swagger_auto_schema(
        tags=['images'],
        operation_id='api_upload_image',
        responses={
            201: 'Image successfully uploaded',
            400: 'Invalid Data',
        },
        manual_parameters=(AUTHORIZATION_PARAM,),
        request_body=UploadImageSerializer,
    )
    def post(self, request):
        serializer = UploadImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.run_validation(data=request.data)
        try:
            uploaded_image = add_uploaded_image_data(user=request.user, data=data)
            return Response(
                {'message': f'{uploaded_image} successfully uploaded'},
                status=status.HTTP_201_CREATED,
            )
        except APIError:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
