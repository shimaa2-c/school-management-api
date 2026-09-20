from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from core.responses import CustomResponseMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    MeSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
)
from rest_framework import viewsets
from .models import User
from .permissions import IsAdminRole
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    'success': True,
                    'message': 'Logout successful.',
                    'data': None,
                    'errors': None,
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid refresh token.',
                    'data': None,
                    'errors': {
                        'refresh': [
                            'Invalid or expired refresh token.'
                        ]
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)

        return Response(
            {
                'success': True,
                'message': 'Current user retrieved successfully.',
                'data': serializer.data,
                'errors': None,
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: None},
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation failed.',
                    'data': None,
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not request.user.check_password(old_password):
            return Response(
                {
                    'success': False,
                    'message': 'Validation failed.',
                    'data': None,
                    'errors': {
                        'old_password': [
                            'Old password is incorrect.'
                        ]
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if old_password == new_password:
            return Response(
                {
                    'success': False,
                    'message': 'Validation failed.',
                    'data': None,
                    'errors': {
                        'new_password': [
                            'New password must be different from '
                            'the old password.'
                        ]
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.save()

        return Response(
            {
                'success': True,
                'message': 'Password changed successfully.',
                'data': None,
                'errors': None,
            },
            status=status.HTTP_200_OK,
        )
    
class UserViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):
    success_messages = {
        "list": "Users retrieved successfully.",
        "retrieve": "User retrieved successfully.",
        "create": "User created successfully.",
        "update": "User updated successfully.",
        "partial_update": "User updated successfully.",
        "destroy": "User deleted successfully.",
    }
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]