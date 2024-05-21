# estatemaster/managers.py

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number=None, account_type=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, account_type=account_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Устанавливаем значения по умолчанию для необязательных полей
        phone_number = extra_fields.pop('phone_number', '0000000000')
        account_type = extra_fields.pop('account_type', 'individual')

        return self.create_user(email, phone_number=phone_number, account_type=account_type, password=password, **extra_fields)
