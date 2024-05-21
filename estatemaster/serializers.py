# serializers.py
from django.conf import settings
from rest_framework import serializers
from .models import CustomUser
from .exceptions import InvalidDataException, DuplicateFieldException
from django.contrib.auth import get_user_model



User = get_user_model()


class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'phone_number', 'account_type')

    def create(self, validated_data):
        try:
            if CustomUser.objects.filter(phone_number=validated_data['phone_number']).exists():
                raise DuplicateFieldException(detail='Phone number already exists.')
            if len(validated_data['password']) < 5:
                raise InvalidDataException(detail='Password must be at least 5 characters long.')

            user = CustomUser.objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                phone_number=validated_data['phone_number'],
                account_type=validated_data['account_type'],
                password=validated_data['password'],
                is_active = False  # Set the user as inactive

            )
            return user
        except KeyError:
            raise InvalidDataException()
        except CustomUser.DoesNotExist:
            raise InvalidDataException()
        except CustomUser.MultipleObjectsReturned:
            raise DuplicateFieldException()


class CustomUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email','phone_number','first_name','last_name','username','photo','date_of_birth','account_type')  # Убедитесь, что здесь есть поле phone_number