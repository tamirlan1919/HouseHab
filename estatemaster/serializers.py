from django.conf import settings
from djoser.utils import decode_uid
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser

from .mixins import  UserFromTokenMixin
from .models import *
from .exceptions import InvalidDataException, DuplicateFieldException
from django.contrib.auth import get_user_model
from rest_framework import viewsets
User = get_user_model()
from djoser.serializers import ActivationSerializer



class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'phone_number' ,'account_type')

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
                is_active = True  # Set the user as inactive


            )
            return user
        except KeyError:
            raise InvalidDataException()
        except CustomUser.DoesNotExist:
            raise InvalidDataException()
        except CustomUser.MultipleObjectsReturned:
            raise DuplicateFieldException()


class RentalSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalSpecialization
        fields = ['id', 'name']

        def validate_name(self, value):
            if RentalSpecialization.objects.filter(name=value).exists():
                raise serializers.ValidationError("Аренда недвижимости with this name already exists.")
            return value

class MortgageSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageSpecialization
        fields = ['id', 'name']

class OtherServiceSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherServiceSpecialization
        fields = ['id', 'name']

class SaleSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleSpecialization
        fields = ['id', 'name']


from rest_framework import serializers

class ProfessionalProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = ProfessionalProfile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        role = instance.role
        if role == 'developer':
            fields_to_remove = [
                'is_macler', 'place_of_work', 'gender', 'working_hours_start',
                'working_hours_end', 'experience', 'about_me', 'facebook', 'bd', 'first_name'
            ]
        elif role == 'agency':
            fields_to_remove = [
                'is_macler', 'about_me', 'facebook', 'gender',
                'place_of_work', 'date_company', 'how_houses', 'how_houses_building',
                'count_zhk', 'bd', 'first_name'
            ]
        else:  # realtor
            fields_to_remove = [
                'company_name', 'about_company', 'email', 'date_company',
                'how_houses', 'how_houses_building', 'count_zhk'
            ]

        for field in fields_to_remove:
            data.pop(field, None)

        return data

    def update(self, instance, validated_data):
        # Обновление или создание профиля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CustomUserProfileSerializer(serializers.ModelSerializer):
    professional_profile = ProfessionalProfileSerializer(required=False)
    parser_classes = (MultiPartParser, FormParser)  # Правильное место для parser_classes

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'username', 'photo', 'date_of_birth', 'account_type', 'is_confirm', 'professional_profile')

    def update(self, instance, validated_data):
        professional_profile_data = validated_data.pop('professional_profile', None)
        print(professional_profile_data)
        instance = super(CustomUserProfileSerializer, self).update(instance, validated_data)

        # Обновление или создание профессионального профиля, если он существует
        if professional_profile_data:
            prof_profile_instance, created = ProfessionalProfile.objects.get_or_create(user=instance)
            prof_serializer = ProfessionalProfileSerializer(prof_profile_instance, data=professional_profile_data, partial=True)
            if prof_serializer.is_valid(raise_exception=True):
                prof_serializer.save()

        return instance
class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

class PromotionConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionConfig
        fields = '__all__'

class BuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class SaleResidentialSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleResidential
        fields = '__all__'
        read_only_fields = ('user',)


class RentLongAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentLongAdvertisement
        fields = '__all__'
        read_only_fields = ('user',)


class RentDayAdvertisementSerializer( serializers.ModelSerializer):
    class Meta:
        model = RentDayAdvertisement
        fields = '__all__'
        read_only_fields = ('user',)


class SaleCommercialAdvertisementSerializer( serializers.ModelSerializer):
    class Meta:
        model = SaleCommercialAdvertisement
        fields = '__all__'
        read_only_fields = ('user',)


class RentCommercialAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentCommercialAdvertisement
        fields = '__all__'
        read_only_fields = ('user',)


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
    status_code = serializers.IntegerField()
    message = serializers.JSONField()


class CustomActivationSerializer(ActivationSerializer):
    def validate(self, attrs):
        uid = decode_uid(attrs['uid'])
        user = User.objects.get(id=uid)

        user.is_confirm = True
        user.save()
        return super().validate(attrs)