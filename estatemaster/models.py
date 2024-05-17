from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    account_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('professional', 'Professional')])

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
