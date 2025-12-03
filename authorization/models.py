from django.db import models
from users.models import User


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        db_table = 'roles'
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')

    class Meta:
        db_table = 'user_roles'
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class BusinessElement(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        db_table = 'business_elements'
        verbose_name = 'Бизнес-объект'
        verbose_name_plural = 'Бизнес-объекты'

    def __str__(self):
        return self.name


class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='access_rules')
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE, related_name='access_rules')
    read_permission = models.BooleanField(default=False, verbose_name='Чтение своих')
    read_all_permission = models.BooleanField(default=False, verbose_name='Чтение всех')
    create_permission = models.BooleanField(default=False, verbose_name='Создание')
    update_permission = models.BooleanField(default=False, verbose_name='Обновление своих')
    update_all_permission = models.BooleanField(default=False, verbose_name='Обновление всех')
    delete_permission = models.BooleanField(default=False, verbose_name='Удаление своих')
    delete_all_permission = models.BooleanField(default=False, verbose_name='Удаление всех')

    class Meta:
        db_table = 'access_rules'
        verbose_name = 'Правило доступа'
        verbose_name_plural = 'Правила доступа'
        unique_together = ['role', 'element']

    def __str__(self):
        return f"{self.role.name} -> {self.element.name}"
