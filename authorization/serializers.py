from rest_framework import serializers
from .models import Role, BusinessElement, AccessRule, UserRole


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ['id', 'name', 'description']


class AccessRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    element_name = serializers.CharField(source='element.name', read_only=True)

    class Meta:
        model = AccessRule
        fields = [
            'id', 'role', 'role_name', 'element', 'element_name',
            'read_permission', 'read_all_permission', 'create_permission',
            'update_permission', 'update_all_permission',
            'delete_permission', 'delete_all_permission'
        ]


class AccessRuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRule
        fields = [
            'role', 'element', 'read_permission', 'read_all_permission', 'create_permission',
            'update_permission', 'update_all_permission', 'delete_permission', 'delete_all_permission'
        ]

    def validate(self, data):
        if self.instance is None:
            if AccessRule.objects.filter(role=data.get('role'), element=data.get('element')).exists():
                raise serializers.ValidationError("Правило для этой роли и элемента уже существует")
        return data


class UserRoleSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'user_email', 'role', 'role_name']
