# serializers.py
from rest_framework import serializers
from .models import CustomUser
from .exceptions import InvalidDataException, DuplicateFieldException

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
                password=validated_data['password']
            )
            return user
        except KeyError:
            raise InvalidDataException()
        except CustomUser.DoesNotExist:
            raise InvalidDataException()
        except CustomUser.MultipleObjectsReturned:
            raise DuplicateFieldException()