from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import User, Session
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserUpdateSerializer
)
from .jwt_utils import generate_jwt_token
from authorization.models import Role, UserRole


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            default_role = Role.objects.filter(name='user').first()
            if default_role:
                UserRole.objects.create(user=user, role=default_role)
            token = generate_jwt_token(user.id)
            return Response({
                'message': 'Регистрация успешна',
                'user': UserSerializer(user).data,
                'token': token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Неверный email или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                return Response({'error': 'Аккаунт деактивирован'}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                return Response({'error': 'Неверный email или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

            token = generate_jwt_token(user.id)
            expires_at = timezone.now() + timedelta(hours=24)
            session = Session.create_session(user, expires_at)

            response = Response({
                'message': 'Вход выполнен успешно',
                'user': UserSerializer(user).data,
                'token': token
            })
            response.set_cookie('session_id', session.session_token, expires=expires_at, httponly=True, samesite='Lax')
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)

        session_token = request.COOKIES.get('session_id')
        if session_token:
            Session.objects.filter(session_token=session_token).delete()

        response = Response({'message': 'Выход выполнен успешно'})
        response.delete_cookie('session_id')
        return response


class MeView(APIView):
    def get(self, request):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(request.current_user).data)

    def put(self, request):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserUpdateSerializer(request.current_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Профиль обновлен', 'user': UserSerializer(request.current_user).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.current_user
        user.is_active = False
        user.save()
        Session.objects.filter(user=user).delete()

        response = Response({'message': 'Аккаунт деактивирован'})
        response.delete_cookie('session_id')
        return response
