from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    account_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('professional', 'Professional')],
                                    default='individual')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'account_type']
    objects = CustomUserManager()  # Используем кастомный менеджер для этой модели пользователя




    # Добавляем related_name для связей с группами и правами доступа
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

    def save(self, *args, **kwargs):
        # Добавляем вашу логику перед сохранением пользователя
        # Например, проверяем или обновляем что-то
        # Здесь просто вызываем метод save родительского класса, чтобы сохранить объект
        super().save(*args, **kwargs)

        # Создаем или обновляем соответствующего пользователя в стандартной модели User
        User = get_user_model()
        user, created = User.objects.update_or_create(
            email=self.email,
            defaults={
                'username': self.email,
                'email': self.email,
                'password': self.password,  # Если нужно, убедитесь, что пароль установлен правильно
            }
        )