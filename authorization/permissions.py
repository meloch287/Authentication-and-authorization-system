from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from .models import AccessRule, UserRole


def get_user_permissions(user, element_name: str) -> dict:
    if not user:
        return {}

    user_roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)
    rules = AccessRule.objects.filter(role_id__in=user_roles, element__name=element_name)

    permissions = {
        'read': False, 'read_all': False, 'create': False,
        'update': False, 'update_all': False, 'delete': False, 'delete_all': False,
    }

    for rule in rules:
        permissions['read'] = permissions['read'] or rule.read_permission
        permissions['read_all'] = permissions['read_all'] or rule.read_all_permission
        permissions['create'] = permissions['create'] or rule.create_permission
        permissions['update'] = permissions['update'] or rule.update_permission
        permissions['update_all'] = permissions['update_all'] or rule.update_all_permission
        permissions['delete'] = permissions['delete'] or rule.delete_permission
        permissions['delete_all'] = permissions['delete_all'] or rule.delete_all_permission

    return permissions


def has_role(user, role_name: str) -> bool:
    if not user:
        return False
    return UserRole.objects.filter(user=user, role__name=role_name).exists()


def require_auth(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(self, request, *args, **kwargs)
    return wrapper


def require_permission(element_name: str, permission_type: str):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if not request.current_user:
                return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)

            permissions = get_user_permissions(request.current_user, element_name)
            if not permissions.get(permission_type, False):
                return Response({'error': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)

            request.permissions = permissions
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def require_admin(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.current_user:
            return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)
        if not has_role(request.current_user, 'admin'):
            return Response({'error': 'Доступ запрещен. Требуется роль администратора'}, status=status.HTTP_403_FORBIDDEN)
        return view_func(self, request, *args, **kwargs)
    return wrapper
