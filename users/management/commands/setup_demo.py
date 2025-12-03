from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import User
from authorization.models import Role, UserRole


class Command(BaseCommand):
    help = 'Setup demo data'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка начальных данных...')

        try:
            call_command('loaddata', 'initial_data', verbosity=0)
            call_command('loaddata', 'access_rules', verbosity=0)
            self.stdout.write(self.style.SUCCESS('Фикстуры загружены'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Фикстуры: {e}'))

        test_users = [
            {'email': 'admin@example.com', 'password': 'admin123', 'first_name': 'Админ', 'last_name': 'Админов', 'role': 'admin'},
            {'email': 'manager@example.com', 'password': 'manager123', 'first_name': 'Менеджер', 'last_name': 'Менеджеров', 'role': 'manager'},
            {'email': 'user@example.com', 'password': 'user123', 'first_name': 'Пользователь', 'last_name': 'Пользователев', 'role': 'user'},
        ]

        for user_data in test_users:
            role_name = user_data.pop('role')
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(email=user_data['email'], defaults=user_data)
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'  Создан: {user.email}')
            role = Role.objects.filter(name=role_name).first()
            if role:
                UserRole.objects.get_or_create(user=user, role=role)

        self.stdout.write(self.style.SUCCESS('\nДемо-данные готовы!'))
        self.stdout.write('  admin@example.com / admin123')
        self.stdout.write('  manager@example.com / manager123')
        self.stdout.write('  user@example.com / user123')
