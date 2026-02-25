from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ClientSerializer
)
from courses.models import Client


class RegisterAPIView(APIView):
    """API для регистрации пользователя"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Создаем JWT токены
            refresh = RefreshToken.for_user(user)

            return Response({
                'status': 'success',
                'message': 'Пользователь успешно зарегистрирован',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """API для авторизации пользователя"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)

                return Response({
                    'status': 'success',
                    'message': 'Авторизация успешна',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })

            return Response({
                'status': 'error',
                'message': 'Неверные учетные данные'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """API для выхода из системы"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({
                'status': 'success',
                'message': 'Выход выполнен успешно'
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    """API для получения данных текущего пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        # Получаем профиль клиента, если он есть
        try:
            client = Client.objects.get(user=user)
            client_data = ClientSerializer(client).data
        except Client.DoesNotExist:
            client_data = None

        return Response({
            'user': serializer.data,
            'profile': client_data
        })


class UserProfileAPIView(APIView):
    """API для работы с профилем пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            client = Client.objects.get(user=request.user)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Профиль не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
            client = Client.objects.get(user=request.user)
            serializer = ClientSerializer(client, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Профиль обновлен',
                    'data': serializer.data
                })

            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Client.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Профиль не найден'
            }, status=status.HTTP_404_NOT_FOUND)