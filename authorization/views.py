from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Role, BusinessElement, AccessRule, UserRole
from .serializers import (
    RoleSerializer, BusinessElementSerializer, AccessRuleSerializer,
    AccessRuleCreateSerializer, UserRoleSerializer
)
from .permissions import require_admin


class RoleListView(APIView):
    @require_admin
    def get(self, request):
        return Response(RoleSerializer(Role.objects.all(), many=True).data)

    @require_admin
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleDetailView(APIView):
    @require_admin
    def get(self, request, pk):
        try:
            return Response(RoleSerializer(Role.objects.get(pk=pk)).data)
        except Role.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)

    @require_admin
    def put(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @require_admin
    def delete(self, request, pk):
        try:
            Role.objects.get(pk=pk).delete()
            return Response({'message': 'Роль удалена'}, status=status.HTTP_204_NO_CONTENT)
        except Role.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)


class BusinessElementListView(APIView):
    @require_admin
    def get(self, request):
        return Response(BusinessElementSerializer(BusinessElement.objects.all(), many=True).data)


class AccessRuleListView(APIView):
    @require_admin
    def get(self, request):
        rules = AccessRule.objects.select_related('role', 'element').all()
        return Response(AccessRuleSerializer(rules, many=True).data)

    @require_admin
    def post(self, request):
        serializer = AccessRuleCreateSerializer(data=request.data)
        if serializer.is_valid():
            rule = serializer.save()
            return Response(AccessRuleSerializer(rule).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessRuleDetailView(APIView):
    @require_admin
    def get(self, request, pk):
        try:
            rule = AccessRule.objects.select_related('role', 'element').get(pk=pk)
            return Response(AccessRuleSerializer(rule).data)
        except AccessRule.DoesNotExist:
            return Response({'error': 'Правило не найдено'}, status=status.HTTP_404_NOT_FOUND)

    @require_admin
    def put(self, request, pk):
        try:
            rule = AccessRule.objects.get(pk=pk)
        except AccessRule.DoesNotExist:
            return Response({'error': 'Правило не найдено'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AccessRuleCreateSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(AccessRuleSerializer(rule).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @require_admin
    def delete(self, request, pk):
        try:
            AccessRule.objects.get(pk=pk).delete()
            return Response({'message': 'Правило удалено'}, status=status.HTTP_204_NO_CONTENT)
        except AccessRule.DoesNotExist:
            return Response({'error': 'Правило не найдено'}, status=status.HTTP_404_NOT_FOUND)


class UserRoleListView(APIView):
    @require_admin
    def get(self, request):
        user_roles = UserRole.objects.select_related('user', 'role').all()
        return Response(UserRoleSerializer(user_roles, many=True).data)

    @require_admin
    def post(self, request):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRoleDetailView(APIView):
    @require_admin
    def delete(self, request, pk):
        try:
            UserRole.objects.get(pk=pk).delete()
            return Response({'message': 'Роль удалена у пользователя'}, status=status.HTTP_204_NO_CONTENT)
        except UserRole.DoesNotExist:
            return Response({'error': 'Связь не найдена'}, status=status.HTTP_404_NOT_FOUND)
