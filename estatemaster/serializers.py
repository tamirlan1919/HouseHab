import uuid

from django.conf import settings
from djoser.utils import decode_uid
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

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



class ProfessionalProfileSerializer(serializers.ModelSerializer):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded_fields = {'user', 'id'}  # Set of fields to exclude
        # Dynamically adjust fields to include by removing excluded ones
        for field_name in excluded_fields:
            self.fields.pop(field_name, None)

    class Meta:
        model = ProfessionalProfile
        fields = '__all__'  # Initially set to include all, but will exclude dynamically in __init__
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
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rental_types'] = instance.rental_types.split(',') if instance.rental_types else []
        representation['mortgage_types'] = instance.mortgage_types.split(',') if instance.mortgage_types else []
        representation['other_services'] = instance.other_services.split(',') if instance.other_services else []
        representation['sale_types'] = instance.sale_types.split(',') if instance.sale_types else []
        return representation

    def to_internal_value(self, data):
        data['rental_types'] = ','.join(data.get('rental_types', []))
        data['mortgage_types'] = ','.join(data.get('mortgage_types', []))
        data['other_services'] = ','.join(data.get('other_services', []))
        data['sale_types'] = ','.join(data.get('sale_types', []))
        return super().to_internal_value(data)

class CustomUserProfileSerializer(serializers.ModelSerializer):
    professional_profile = ProfessionalProfileSerializer(required=False)
    parser_classes = (MultiPartParser, FormParser)  # Правильное место для parser_classes

    class Meta:
        model = CustomUser
        fields = ('id', 'email' ,'phone_number', 'first_name', 'last_name', 'username', 'photo', 'date_of_birth', 'account_type', 'is_confirm', 'professional_profile')

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

class AdvertisementPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementPhoto
        fields = ['id', 'image', 'user']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        # Устанавливаем пользователя из контекста запроса
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PhotoGroupSerializer(serializers.ModelSerializer):
    photos = AdvertisementPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = PhotoGroup
        fields = ['id', 'created_at', 'photos']

class SaleSellerContactsField(serializers.Field):
    def to_representation(self, value):
        return {
            'phone': value.phone,
            'whatsApp': value.whatsApp
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'phone' not in data or 'whatsApp' not in data:
            raise serializers.ValidationError("Invalid data format for 'sellerContacts'. Expected a dictionary with 'phone' and 'whatsApp'.")
        return {
            'phone': data.get('phone'),
            'whatsApp': data.get('whatsApp')
        }

class SaleGetPrice(serializers.Field):
    def to_representation(self, value):
        return {
            'value': value.price,
            'currency': value.currency
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'value' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'sellerContacts'. Expected a dictionary with 'phone' and 'whatsApp'.")
        return {
            'price': data.get('value'),
            'currency': data.get('currency')
        }

class SaleResidentialSerializer(serializers.ModelSerializer):
    photos = AdvertisementPhotoSerializer(many=True, read_only=True)
    photo_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    price = SaleGetPrice(source='*')
    sellerContacts = SaleSellerContactsField(source='*')
    viewFromWindow = serializers.ListField(
        child=serializers.ChoiceField(choices=['outside', 'courtyard', 'atSea']),
        write_only=True
    )
    class Meta:
        model = SaleResidential
        fields = [
            'id',
            'user',
            'accountType',
            'dealType',
            'estateType',
            'obj',
            'nearestStop',
            'minutesBusStop',
            'address',
            'pathType',
            'floor',
            'floorsHouse',
            'flatNumber',
            'yearBuilt',
            'ceilingHeight',
            'houseType',
            'roomsNumber',
            'totalArea',
            'livingArea',
            'kitchenArea',
            'propertyType',
            'photos',
            'youtubeLink',
            'balconies',
            'loggia',
            'viewFromWindow',
            'separateBathroom',
            'repair',
            'freightElevator',
            'passengerElevator',
            'combinedBathroom',
            'apartmentEntrance',
            'parking',
            'title',
            'description',
            'price',  # This will now handle both value and currency
            'saleType',
            'sellerContacts',
            'photo_ids',  # Добавляем photo_ids в список полей
            'created_at'
        ]
        read_only_fields = ('user',)

    def create(self, validated_data):
        # Обработка данных о цене
        price_data = validated_data.pop('price', None)
        if isinstance(price_data, dict):
            validated_data['price'] = price_data.get('value')
            validated_data['currency'] = price_data.get('currency')
        elif isinstance(price_data, int):  # Если цена уже целое число
            validated_data['price'] = price_data

        # Извлечение и обработка идентификаторов фотографий
        photo_ids = validated_data.pop('photo_ids', [])

        # Обработка MultiSelectField данных
        # view_from_window = validated_data.get('viewFromWindow')
        # if view_from_window and not isinstance(view_from_window, list):
        #     validated_data['viewFromWindow'] = [view_from_window]

        apartment_entrance = validated_data.get('apartmentEntrance')
        if apartment_entrance and not isinstance(apartment_entrance, list):
            validated_data['apartmentEntrance'] = [apartment_entrance]

        # Установка пользователя из контекста запроса
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user

        # Создание объекта SaleResidential
        sale_residential = super().create(validated_data)

        # Связывание фотографий с созданным объектом SaleResidential
        if photo_ids:
            content_type = ContentType.objects.get_for_model(SaleResidential)
            AdvertisementPhoto.objects.filter(id__in=photo_ids, user=request.user).update(
                content_type=content_type,
                object_id=sale_residential.id
            )

        return sale_residential

    def update(self, instance, validated_data):
        # Обработка данных о цене
        price_data = validated_data.pop('price', None)
        if price_data:
            instance.price = price_data.get('value', instance.price)
            instance.currency = price_data.get('currency', instance.currency)

        # Обработка MultiSelectField данных
        view_from_window = validated_data.get('viewFromWindow')

        if view_from_window and not isinstance(view_from_window, list):
            validated_data['viewFromWindow'] = [view_from_window]

        apartment_entrance = validated_data.get('apartmentEntrance')
        if apartment_entrance and not isinstance(apartment_entrance, list):
            validated_data['apartmentEntrance'] = [apartment_entrance]

        # Обновляем другие поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class MonthlyRentField(serializers.Field):
    def to_representation(self, value):
        return {
            'price': value.rent_per_month,
            'currency': value.currency_per_month
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'price' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'monthlyRent'. Expected a dictionary with 'value' and 'currency'.")
        return {
            'rent_per_month': data.get('price'),
            'currency_per_month': data.get('currency')
        }

# Кастомное поле для deposit
class DepositRentField(serializers.Field):
    def to_representation(self, value):
        return {
            'price': value.deposit,
            'currency': value.currency
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'price' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'deposit'. Expected a dictionary with 'value' and 'currency'.")
        return {
            'deposit': data.get('price'),
            'currency': data.get('currency')
        }

# Кастомное поле для sellerContacts
class SellerContactsField(serializers.Field):
    def to_representation(self, value):
        return {
            'phone': value.phone,
            'whatsApp': value.whatsApp
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'phone' not in data or 'whatsApp' not in data:
            raise serializers.ValidationError("Invalid data format for 'sellerContacts'. Expected a dictionary with 'phone' and 'whatsApp'.")
        return {
            'phone': data.get('phone'),
            'whatsApp': data.get('whatsApp')
        }

# Основной сериализатор для RentLongAdvertisement
class RentLongAdvertisementSerializer(serializers.ModelSerializer):
    photos = AdvertisementPhotoSerializer(many=True, read_only=True)
    photo_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    monthlyRent = MonthlyRentField(source='*')
    deposit = DepositRentField(source='*')
    sellerContacts = SellerContactsField(source='*')
    furniture = serializers.ListField(
        child=serializers.ChoiceField(choices=['inKitchen', 'inRooms', 'noFurniture']),
        write_only=True
    )
    bathroom = serializers.ListField(
        child=serializers.ChoiceField(choices=['bath', 'showerRoom']),
        write_only=True
    )
    apartment = serializers.ListField(
        child=serializers.ChoiceField(choices=['conditioner', 'fridge', 'tv', 'dishwasher', 'washingMachine']),
        write_only=True
    )
    connection = serializers.ListField(
        child=serializers.ChoiceField(choices=['internet', 'phone']),
        write_only=True
    )

    class Meta:
        model = RentLongAdvertisement
        fields = [
            'id',
            'accountType',
            'dealType',
            'estateType',
            'leaseType',
            'obj',
            'nearestStop',
            'minutesBusStop',
            'address',
            'pathType',
            'roomsNumber',
            'floor',
            'floorsHouse',
            'flatNumber',
            'totalArea',
            'livingArea',
            'kitchenArea',
            'propertyType',
            'youtubeLink',
            'photos',
            'viewFromWindow',
            'balconies',
            'loggia',
            'separateBathroom',
            'combinedBathroom',
            'repair',
            'passengerElevator',
            'freightElevator',
            'apartmentEntrance',
            'parking',
            'utilityPayment',
            'prepaymentPeriod',
            'rentalTerm',
            'livingConditions',
            'furniture',
            'bathroom',
            'apartment',
            'connection',
            'title',
            'description',
            'user',
            'monthlyRent',
            'deposit',
            'sellerContacts',
            'photo_ids',
            'created_at'
        ]
        read_only_fields = ('user',)

    def to_internal_value(self, data):
        """Handle incoming data for POST/PUT requests"""

        # Validate 'furniture' field
        furniture_data = data.get('furniture')
        if furniture_data:
            if 'noFurniture' in furniture_data and len(furniture_data) > 1:
                raise serializers.ValidationError({'furniture': "'noFurniture' cannot be combined with other options."})
            valid_furniture_choices = ['noFurniture', 'inKitchen', 'inRooms']
            for item in furniture_data:
                if item not in valid_furniture_choices:
                    raise serializers.ValidationError({'furniture': f"'{item}' is not a valid choice for furniture."})

        # Validate 'bathroom' field
        bathroom_data = data.get('bathroom')
        if bathroom_data:
            valid_bathroom_choices = ['bath', 'showerRoom']
            for item in bathroom_data:
                if item not in valid_bathroom_choices:
                    raise serializers.ValidationError({'bathroom': f"'{item}' is not a valid choice for bathroom."})

        # Validate 'apartment' field
        apartment_data = data.get('apartment')
        if apartment_data:
            valid_apartment_choices = ['conditioner', 'fridge', 'tv', 'dishwasher', 'washingMachine']
            for item in apartment_data:
                if item not in valid_apartment_choices:
                    raise serializers.ValidationError({'apartment': f"'{item}' is not a valid choice for apartment."})

        # Validate 'connection' field
        connection_data = data.get('connection')
        if connection_data:
            valid_connection_choices = ['internet', 'phone']
            for item in connection_data:
                if item not in valid_connection_choices:
                    raise serializers.ValidationError({'connection': f"'{item}' is not a valid choice for connection."})

        # Call the parent's to_internal_value method to handle other fields
        return super().to_internal_value(data)

    def create(self, validated_data):
        # Handle nested fields for creation
        photo_ids = validated_data.pop('photo_ids', [])


        apartment_entrance = validated_data.get('apartmentEntrance')
        if apartment_entrance and not isinstance(apartment_entrance, list):
            validated_data['apartmentEntrance'] = [apartment_entrance]

        # Set the user from the request context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user



        # Create the RentLongAdvertisement instance
        rent_long_advertisement = super().create(validated_data)

        # Associate photos
        if photo_ids:
            content_type = ContentType.objects.get_for_model(RentLongAdvertisement)
            AdvertisementPhoto.objects.filter(id__in=photo_ids).update(
                content_type=content_type,
                object_id=rent_long_advertisement.id
            )

        return rent_long_advertisement

    def update(self, instance, validated_data):
        # Handle nested fields for update
        monthly_rent_data = validated_data.pop('monthlyRent', None)
        if monthly_rent_data:
            instance.rent_per_month = monthly_rent_data.get('value', instance.rent_per_month)
            instance.currency_per_month = monthly_rent_data.get('currency', instance.currency_per_month)

        deposit_data = validated_data.pop('deposit', None)
        if deposit_data:
            instance.deposit = deposit_data.get('value', instance.deposit)
            instance.currency = deposit_data.get('currency', instance.currency)

        seller_contacts_data = validated_data.pop('sellerContacts', None)
        if seller_contacts_data:
            instance.phone = seller_contacts_data.get('phone', instance.phone)
            instance.whatsApp = seller_contacts_data.get('whatsApp', instance.whatsApp)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class DailyRentField(serializers.Field):
    def to_representation(self, value):
        return {
            'value': value.daily_price,
            'currency': value.daily_price_currency
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'value' not in data or 'currency' not in data:
            raise serializers.ValidationError(
                "Invalid data format for 'price'. Expected a dictionary with 'value' and 'currency'.")
        return {
            'daily_price': data.get('value'),
            'daily_price_currency': data.get('currency')
        }


# Кастомное поле для deposit
class DepositDayRentField(serializers.Field):
    def to_representation(self, value):
        return {
            'price': value.deposit,
            'currency': value.deposit_currency
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'price' not in data or 'currency' not in data:
            raise serializers.ValidationError(
                "Invalid data format for 'deposit'. Expected a dictionary with 'price' and 'currency'.")
        return {
            'deposit': data.get('price'),
            'deposit_currency': data.get('currency')
        }


# Кастомное поле для sellerContacts
class SellerDayRentContactsField(serializers.Field):
    def to_representation(self, value):
        return {
            'phone': value.phone,
            'whatsApp': value.whatsApp
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'phone' not in data or 'whatsApp' not in data:
            raise serializers.ValidationError(
                "Invalid data format for 'sellerContacts'. Expected a dictionary with 'phone' and 'whatsApp'.")
        return {
            'phone': data.get('phone'),
            'whatsApp': data.get('whatsApp')
        }


# Основной сериализатор для RentDayAdvertisement
class RentDayAdvertisementSerializer(serializers.ModelSerializer):
    photos = AdvertisementPhotoSerializer(many=True, read_only=True)
    photo_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    price = DailyRentField(source='*')
    deposit = DepositDayRentField(source='*')
    sellerContacts = SellerDayRentContactsField(source='*')

    furniture = serializers.ListField(
        child=serializers.ChoiceField(choices=['inKitchen', 'inRooms', 'noFurniture']),
        write_only=True,
        required=False,
        allow_empty=True
    )
    bathroom_choice = serializers.ListField(
        child=serializers.ChoiceField(choices=['bath', 'showerRoom']),
        write_only=True,
        required=False,
        allow_empty=True
    )
    tech = serializers.ListField(
        child=serializers.ChoiceField(choices=['conditioner', 'fridge', 'tv', 'dishwasher', 'washingMachine']),
        write_only=True,
        required=False,
        allow_empty=True
    )
    communication = serializers.ListField(
        child=serializers.ChoiceField(choices=['internet', 'phone']),
        write_only=True,
        required=False,
        allow_empty=True
    )
    living_conditions = serializers.ListField(
        child=serializers.ChoiceField(choices=['allowed_with_children', 'allowed_with_pets']),
        write_only=True,
        required=False,
        allow_empty=True
    )

    class Meta:
        model = RentDayAdvertisement
        fields = [
            'id',
            'accountType',
            'dealType',
            'estateType',
            'leaseType',
            'obj',
            'region',
            'address',
            'nearestStop',
            'minutesBusStop',
            'pathType',
            'floor',
            'floorsHouse',
            'flatNumber',
            'roomsNumber',
            'totalArea',
            'livingArea',
            'kitchenArea',
            'propertyType',
            'photos',
            'youtubeLink',
            'title',
            'description',
            'price',
            'deposit',
            'furniture',
            'bathroom_choice',
            'tech',
            'communication',
            'living_conditions',
            'sellerContacts',
            'user',
            'photo_ids',
            'created_at'
        ]
        read_only_fields = ('user',)

    def to_internal_value(self, data):
        """Handle incoming data for POST/PUT requests"""

        # Validate 'furniture' field
        furniture_data = data.get('furniture')
        if furniture_data:
            if 'noFurniture' in furniture_data and len(furniture_data) > 1:
                raise serializers.ValidationError({'furniture': "'noFurniture' cannot be combined with other options."})
            valid_furniture_choices = ['noFurniture', 'inKitchen', 'inRooms']
            for item in furniture_data:
                if item not in valid_furniture_choices:
                    raise serializers.ValidationError({'furniture': f"'{item}' is not a valid choice for furniture."})

        # Validate 'bathroom_choice' field
        bathroom_data = data.get('bathroom_choice')
        if bathroom_data:
            valid_bathroom_choices = ['bath', 'showerRoom']
            for item in bathroom_data:
                if item not in valid_bathroom_choices:
                    raise serializers.ValidationError(
                        {'bathroom_choice': f"'{item}' is not a valid choice for bathroom."})

        # Validate 'tech' field
        tech_data = data.get('tech')
        if tech_data:
            valid_tech_choices = ['conditioner', 'fridge', 'tv', 'dishwasher', 'washingMachine']
            for item in tech_data:
                if item not in valid_tech_choices:
                    raise serializers.ValidationError({'tech': f"'{item}' is not a valid choice for tech."})

        # Validate 'communication' field
        communication_data = data.get('communication')
        if communication_data:
            valid_communication_choices = ['internet', 'phone']
            for item in communication_data:
                if item not in valid_communication_choices:
                    raise serializers.ValidationError(
                        {'communication': f"'{item}' is not a valid choice for communication."})

        # Validate 'living_conditions' field
        living_conditions_data = data.get('living_conditions')
        if living_conditions_data:
            valid_living_conditions_choices = ['allowed_with_children', 'allowed_with_pets']
            for item in living_conditions_data:
                if item not in valid_living_conditions_choices:
                    raise serializers.ValidationError(
                        {'living_conditions': f"'{item}' is not a valid choice for living conditions."})

        return super().to_internal_value(data)

    def create(self, validated_data):
        # Handle nested fields for creation
        photo_ids = validated_data.pop('photo_ids', [])

        # Set the user from the request context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user

        # Create the RentDayAdvertisement instance
        rent_day_advertisement = super().create(validated_data)

        # Associate photos
        if photo_ids:
            content_type = ContentType.objects.get_for_model(RentDayAdvertisement)
            AdvertisementPhoto.objects.filter(id__in=photo_ids).update(
                content_type=content_type,
                object_id=rent_day_advertisement.id
            )

        return rent_day_advertisement

    def update(self, instance, validated_data):
        # Handle nested fields for update
        daily_rent_data = validated_data.pop('price', None)
        if daily_rent_data:
            instance.daily_price = daily_rent_data.get('value', instance.daily_price)
            instance.daily_price_currency = daily_rent_data.get('currency', instance.daily_price_currency)

        deposit_data = validated_data.pop('deposit', None)
        if deposit_data:
            instance.deposit = deposit_data.get('value', instance.deposit)
            instance.deposit_currency = deposit_data.get('currency', instance.deposit_currency)

        seller_contacts_data = validated_data.pop('sellerContacts', None)
        if seller_contacts_data:
            instance.phone = seller_contacts_data.get('phone', instance.phone)
            instance.whatsApp = seller_contacts_data.get('whatsApp', instance.whatsApp)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance




# Кастомные поля для сериализатора
class PriceForAllField(serializers.Field):
    def to_representation(self, value):
        return {
            'value': value.total_price,
            'currency': value.currency_total
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'value' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'priceForAll'. Expected a dictionary with 'value' and 'currency'.")
        return {
            'total_price': data.get('value'),
            'currency_total': data.get('currency')
        }

class PriceForM2Field(serializers.Field):
    def to_representation(self, value):
        return {
            'value': value.price_per_m2,
            'currency': value.currency_per
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'value' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'priceForM2'. Expected a dictionary with 'value' and 'currency'.")
        return {
            'price_per_m2': data.get('value'),
            'currency_per': data.get('currency')
        }

class ParkingPriceField(serializers.Field):
    def to_representation(self, value):
        return {
            'value': value.parkingPrice,
            'currency': value.parkingCurreny
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'value' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'parkingPrice'. Expected a dictionary with 'value' and 'currency'.")
        return {
            'parkingPrice': data.get('value'),
            'parkingCurreny': data.get('currency')
        }

class SellerСommercialContactsField(serializers.Field):
    def to_representation(self, value):
        return {
            'phone': value.phone,
            'whatsApp': value.whatsApp
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'phone' not in data or 'whatsApp' not in data:
            raise serializers.ValidationError("Invalid data format for 'sellerContacts'. Expected a dictionary with 'phone' and 'whatsApp'.")
        return {
            'phone': data.get('phone'),
            'whatsApp': data.get('whatsApp')
        }

# Основной сериализатор для SaleCommercialAdvertisement
class SaleCommercialAdvertisementSerializer(serializers.ModelSerializer):
    photos = AdvertisementPhotoSerializer(many=True, read_only=True)
    photo_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    priceForAll = PriceForAllField(source='*')
    priceForM2 = PriceForM2Field(source='*')
    parkingPrice = ParkingPriceField(source='*')
    sellerContacts = SellerСommercialContactsField(source='*')

    # Добавление ListField для полей с множественным выбором (MultiSelectField)
    infrastructure = serializers.ListField(
        child=serializers.ChoiceField(choices=SaleCommercialAdvertisement.INFRASTRUCTURE_CHOICES),
        write_only=True,
        required=False,
        allow_empty=True
    )

    class Meta:
        model = SaleCommercialAdvertisement

        fields = [
            'id',
            'user',
            'accountType',
            'dealType',
            'estateType',
            'obj',
            'region',
            'address',
            'nearestStop',
            'minutesBusStop',
            'pathType',
            'taxNumber',
            'totalArea',
            'ceilingHeights',
            'floor',
            'floorsHouse',
            'legalAddress',
            'isRoomOccupied',
            'planning',
            'numberWetSpots',
            'electricPower',
            'status',
            'furniture_c',
            'access',
            'parking',
            'numberParkingPlaces',
            'parkingFees',
            'buildingName',
            'yearBuilt',
            'buildingType',
            'buildingClass',
            'buildingArea',
            'plot',
            'category',
            'developer',
            'managementCompany',
            'ventilation',
            'сonditioning',
            'heating',
            'fireExtinguishingSystem',
            'infrastructure',
            'photos',
            'youtubeLink',
            'title',
            'description',
            'priceForAll',
            'priceForM2',
            'parkingPrice',
            'tax',
            'agentBonus',
            'sellerContacts',
            'photo_ids',
            'created_at'
        ]
        read_only_fields = ('user',)



    def create(self, validated_data):
        # Handle nested fields for creation
        photo_ids = validated_data.pop('photo_ids', [])

        # Set the user from the request context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user

        # Create the SaleCommercialAdvertisement instance
        sale_commercial_advertisement = super().create(validated_data)

        # Associate photos
        if photo_ids:
            content_type = ContentType.objects.get_for_model(SaleCommercialAdvertisement)
            AdvertisementPhoto.objects.filter(id__in=photo_ids).update(
                content_type=content_type,
                object_id=sale_commercial_advertisement.id
            )

        return sale_commercial_advertisement

    def update(self, instance, validated_data):
        # Handle nested fields for update
        price_for_all_data = validated_data.pop('priceForAll', None)
        if price_for_all_data:
            instance.total_price = price_for_all_data.get('value', instance.total_price)
            instance.currency_total = price_for_all_data.get('currency', instance.currency_total)

        price_for_m2_data = validated_data.pop('priceForM2', None)
        if price_for_m2_data:
            instance.price_per_m2 = price_for_m2_data.get('value', instance.price_per_m2)
            instance.currency_per = price_for_m2_data.get('currency', instance.currency_per)

        parking_price_data = validated_data.pop('parkingPrice', None)
        if parking_price_data:
            instance.parkingPrice = parking_price_data.get('value', instance.parkingPrice)
            instance.parkingCurreny = parking_price_data.get('currency', instance.parkingCurreny)

        seller_contacts_data = validated_data.pop('sellerContacts', None)
        if seller_contacts_data:
            instance.phone = seller_contacts_data.get('phone', instance.phone)
            instance.whatsApp = seller_contacts_data.get('whatsApp', instance.whatsApp)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance




# Кастомные поля для сериализатора
class ParkingPriceCommercialField(serializers.Field):
    def to_representation(self, value):
        return {
            'value': value.parkingPrice,
            'currency': value.parkingCurreny
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'value' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'parkingPrice'. Expected a dictionary with 'value' and 'currency'.")
        return {
            'parkingPrice': data.get('value'),
            'parkingCurreny': data.get('currency')
        }

class MonthlyRentCommercialField(serializers.Field):
    def to_representation(self, value):
        return {
            'price': value.rent_per_month,
            'currency': value.currency_rent_month
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'price' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'monthlyRent'. Expected a dictionary with 'price' and 'currency'.")
        return {
            'rent_per_month': data.get('price'),
            'currency_rent_month': data.get('currency')
        }

class MonthlyRentPerSqMField(serializers.Field):
    def to_representation(self, value):
        return {
            'price': value.rent_per_month_per_m2,
            'currency': value.currency_rent_month_per_m2
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'price' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'monthlyRentPerSqM'. Expected a dictionary with 'price' and 'currency'.")
        return {
            'rent_per_month_per_m2': data.get('price'),
            'currency_rent_month_per_m2': data.get('currency')
        }

class SecurityDepositField(serializers.Field):
    def to_representation(self, value):
        return {
            'price': value.security_deposit,
            'currency': value.currency_deposit
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'price' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'securityDeposit'. Expected a dictionary with 'price' and 'currency'.")
        return {
            'security_deposit': data.get('price'),
            'currency_deposit': data.get('currency')
        }

class SellerContactsCommercialField(serializers.Field):
    def to_representation(self, value):
        return {
            'phone': value.phone,
            'whatsApp': value.whatsApp
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'phone' not in data or 'whatsApp' not in data:
            raise serializers.ValidationError("Invalid data format for 'sellerContacts'. Expected a dictionary with 'phone' and 'whatsApp'.")
        return {
            'phone': data.get('phone'),
            'whatsApp': data.get('whatsApp')
        }

class YearlyRentPerSqMField(serializers.Field):
    def to_representation(self, value):
        return {
            'price': value.rent_per_year_per_m2,
            'currency': value.currency_rent_year_per_m2
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or 'price' not in data or 'currency' not in data:
            raise serializers.ValidationError("Invalid data format for 'yearlyRentPerSqM'. Expected a dictionary with 'price' and 'currency'.")
        return {
            'rent_per_year_per_m2': data.get('price'),
            'currency_rent_year_per_m2': data.get('currency')
        }

# Основной сериализатор для RentCommercialAdvertisement
class RentCommercialAdvertisementSerializer(serializers.ModelSerializer):
    photos = AdvertisementPhotoSerializer(many=True, read_only=True)
    photo_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    parkingPrice = ParkingPriceCommercialField(source='*')
    monthlyRent = MonthlyRentCommercialField(source='*')
    monthlyRentPerSqM = MonthlyRentPerSqMField(source='*')
    securityDeposit = SecurityDepositField(source='*')
    sellerContacts = SellerContactsCommercialField(source='*')
    yearlyRentPerSqM = YearlyRentPerSqMField(source='*')

    # Добавление ListField для полей с множественным выбором (MultiSelectField)
    infrastructure = serializers.ListField(
        child=serializers.ChoiceField(choices=RentCommercialAdvertisement.INFRASTRUCTURE_CHOICES),
        write_only=True,
        required=False,
        allow_empty=True
    )

    class Meta:
        model = RentCommercialAdvertisement
        fields = [
            'id',
            'user',
            'accountType',
            'dealType',
            'estateType',
            'obj',
            'region',
            'address',
            'nearestStop',
            'minutesBusStop',
            'pathType',
            'taxNumber',
            'totalArea',
            'ceilingHeights',
            'floor',
            'floorsHouse',
            'legalAddress',
            'isRoomOccupied',
            'planning',
            'numberWetSpots',
            'electricPower',
            'status',
            'furniture_c',
            'access',
            'parking',
            'numberParkingPlaces',
            'parkingFees',
            'buildingName',
            'yearBuilt',
            'buildingType',
            'buildingClass',
            'buildingArea',
            'plot',
            'category',
            'developer',
            'managementCompany',
            'ventilation',
            'сonditioning',
            'heating',
            'fireExtinguishingSystem',
            'infrastructure',
            'photos',
            'youtubeLink',
            'title',
            'description',
            'tax',
            'utilityPayment',
            'operatingCosts',
            'rentalType',
            'minimumLeaseTerm',
            'rentalHolidays',
            'prepayment',
            'agentBonus',
            'phone',
            'whatsApp',
            'parkingPrice',
            'monthlyRent',
            'monthlyRentPerSqM',
            'securityDeposit',
            'sellerContacts',
            'yearlyRentPerSqM',
            'photo_ids',
            'created_at'
        ]
        read_only_fields = ('user',)




    def create(self, validated_data):
        # Handle nested fields for creation
        photo_ids = validated_data.pop('photo_ids', [])

        # Set the user from the request context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user

        # Create the RentCommercialAdvertisement instance
        rent_commercial_advertisement = super().create(validated_data)

        # Associate photos
        if photo_ids:
            content_type = ContentType.objects.get_for_model(RentCommercialAdvertisement)
            AdvertisementPhoto.objects.filter(id__in=photo_ids).update(
                content_type=content_type,
                object_id=rent_commercial_advertisement.id
            )

        return rent_commercial_advertisement

    def update(self, instance, validated_data):
        # Handle nested fields for update
        parking_price_data = validated_data.pop('parkingPrice', None)
        if parking_price_data:
            instance.parkingPrice = parking_price_data.get('value', instance.parkingPrice)
            instance.parkingCurreny = parking_price_data.get('currency', instance.parkingCurreny)

        monthly_rent_data = validated_data.pop('monthlyRent', None)
        if monthly_rent_data:
            instance.rent_per_month = monthly_rent_data.get('value', instance.rent_per_month)
            instance.currency_rent_month = monthly_rent_data.get('currency', instance.currency_rent_month)

        monthly_rent_per_sq_m_data = validated_data.pop('monthlyRentPerSqM', None)
        if monthly_rent_per_sq_m_data:
            instance.rent_per_month_per_m2 = monthly_rent_per_sq_m_data.get('value', instance.rent_per_month_per_m2)
            instance.currency_rent_month_per_m2 = monthly_rent_per_sq_m_data.get('currency', instance.currency_rent_month_per_m2)

        security_deposit_data = validated_data.pop('securityDeposit', None)
        if security_deposit_data:
            instance.security_deposit = security_deposit_data.get('value', instance.security_deposit)
            instance.currency_deposit = security_deposit_data.get('currency', instance.currency_deposit)

        seller_contacts_data = validated_data.pop('sellerContacts', None)
        if seller_contacts_data:
            instance.phone = seller_contacts_data.get('phone', instance.phone)
            instance.whatsApp = seller_contacts_data.get('whatsApp', instance.whatsApp)

        yearly_rent_per_sq_m_data = validated_data.pop('yearlyRentPerSqM', None)
        if yearly_rent_per_sq_m_data:
            instance.rent_per_year_per_m2 = yearly_rent_per_sq_m_data.get('value', instance.rent_per_year_per_m2)
            instance.currency_rent_year_per_m2 = yearly_rent_per_sq_m_data.get('currency', instance.currency_rent_year_per_m2)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class AllAdvertisementsView(APIView):
    def get(self, request, *args, **kwargs):
        # Собираем данные из разных моделей
        sales_residential = SaleResidential.objects.all()
        rent_long = RentLongAdvertisement.objects.all()
        rent_day = RentDayAdvertisement.objects.all()
        sale_commercial = SaleCommercialAdvertisement.objects.all()
        rent_commercial = RentCommercialAdvertisement.objects.all()

        # Сериализация данных
        sales_residential_data = SaleResidentialSerializer(sales_residential, many=True).data
        rent_long_data = RentLongAdvertisementSerializer(rent_long, many=True).data
        rent_day_data = RentDayAdvertisementSerializer(rent_day, many=True).data
        sale_commercial_data = SaleCommercialAdvertisementSerializer(sale_commercial, many=True).data
        rent_commercial_data = RentCommercialAdvertisementSerializer(rent_commercial, many=True).data

        # Объединяем все в один список
        result_data = {
            'sales_residential': sales_residential_data,
            'rent_long': rent_long_data,
            'rent_day': rent_day_data,
            'sale_commercial': sale_commercial_data,
            'rent_commercial': rent_commercial_data
        }

        return  Response(result_data, status=status.HTTP_200_OK)

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


class FilteredAdvertisementsView(APIView):
    def get(self, request, *args, **kwargs):
        data = request.query_params
        deal_type = data.get('deal_type', None)

        type_of_property = data.get('type_of_property', None)
        print(deal_type, type_of_property)
        filters = {
            'region': data.get('region', None),
            'min_price': data.get('min_price', None),
            'max_price': data.get('max_price', None),
            'min_area': data.get('min_area', None),
            'max_area': data.get('max_area', None),
            'count_rooms': data.get('count_rooms', None),
            'year_built_min': data.get('year_built', None),
            'year_built_max': data.get('year_built', None),


            'furnished': data.get('furnished', None),
            'renovation': data.get('renovation', None),
            'min_rent_period': data.get('min_rent_period', None),
            'obj': data.get('obj', None),
            'address': data.get('address', None),
            'transport': data.get('transport', None),
            'repair': data.get('repair', None),
            'phone': data.get('phone', None),
            'account_type': data.get('account_type',None),
            'minute_stop': data.get('minute_stop',None),
            'kitchen_area_min': data.get('kitchen_area_min', None),
            'kitchen_area_max': data.get('kitchen_area_max', None),
            'property_type': data.get('property_type', None),
            'floor_min': data.get('floor_min', None),
            'floor_max': data.get('floor_max', None),
            'balconies': data.get('balconies', None),
            'loggia': data.get('loggia', None),
            'type_house': data.get('type_house',None),
            'min_area_kitchen': data.get('min_area_kitchen',None),
            'max_area_kitchen': data.get('max_area_kitchen',None),
            'price_all_min': data.get('price_all_min',None),
            'price_all_max': data.get('price_all_max',None),
            'price_kv_m_min': data.get('price_kv_m_min', None),
            'price_kv_m_max': data.get('price_kv_m_max', None),
            'new_or_no': data.get('new_or_no',None)


        }

        # Создаем пустой список, куда будем добавлять результаты
        results = []

        # Функция для применения общих фильтров
        def apply_filters(queryset):
            materials = filters.getlist('material')
            if filters['region']:
                queryset = queryset.filter(address__icontains=filters['region'])
            if filters['balconies']:
                queryset = queryset.filter(balconies=filters['balconies'])
            if filters['loggia']:
                queryset = queryset.filter(loggia=filters['loggia'])
            if deal_type:
                queryset = queryset.filter(deal_type=deal_type)
            if type_of_property:
                queryset = queryset.filter(type_of_property=type_of_property)

            # Проверка и фильтрация по цене (за все или за кв. м.)

            if filters.get('price_all_min'):
                queryset = queryset.filter(price_all__gte=filters['price_all_min'])
            if filters.get('price_all_max'):
                queryset = queryset.filter(price_all__lte=filters['price_all_max'])
            if filters.get('price_kv_m_min'):
                queryset = queryset.filter(price_kv_m__gte=filters['price_kv_m_min'])
            if filters.get('price_kv_m_max'):
                queryset = queryset.filter(price_kv_m__lte=filters['price_kv_m_max'])

            if filters['account_type'] == 'owner':
                queryset = queryset.filter(account_type=filters['account_type'])
            if filters['new_or_no']:
                queryset = queryset.filter(new_or_no=filters['new_or_no'])

            if filters['min_area_kitchen']:
                queryset = queryset.filter(kitchen_area__gte=filters['min_area_kitchen'])
            if filters['max_area_kitchen']:
                queryset = queryset.filter(kitchen_area__lte=filters['max_area_kitchen'])

            if filters['min_area']:
                queryset = queryset.filter(total_area__gte=filters['min_area'])
            if filters['max_area']:
                queryset = queryset.filter(total_area__lte=filters['max_area'])
            if 'count_rooms' in filters and filters['count_rooms']:
                # Преобразование строки с номерами комнат в список
                room_counts = filters['count_rooms'].split(',')
                queryset = queryset.filter(count_rooms__in=room_counts)
            if filters['property_type']:
                queryset = queryset.filter(property_type=filters['property_type'])
            if filters['minute_stop']:
                queryset = queryset.filter(minute_stop=filters['minute_stop'])
            if filters['year_built_min']:
                queryset = queryset.filter(age_build__gte=filters['year_built_min'])
            if filters['year_built_max']:
                queryset = queryset.filter(age_build__lte=filters['year_built_max'])

            if materials:
                queryset = queryset.filter(type_house__in=materials)
            if filters['floor_min']:
                queryset = queryset.filter(floor__gte=filters['floor_min'])
            if filters['floor_max']:
                queryset = queryset.filter(floor__lte=filters['floor_max'])
            if filters['furnished']:
                queryset = queryset.filter(without_mebel=filters['furnished'])
            if filters['renovation']:
                queryset = queryset.filter(repair=filters['renovation'])
            if filters['min_rent_period']:
                queryset = queryset.filter(min_rent_period__gte=filters['min_rent_period'])
            if filters['obj']:
                queryset = queryset.filter(obj=filters['obj'])
            if filters['address']:
                queryset = queryset.filter(address__icontains=filters['address'])
            if filters['transport']:
                queryset = queryset.filter(transport=filters['transport'])
            if filters['repair']:
                queryset = queryset.filter(repair=filters['repair'])
            if filters['phone']:
                queryset = queryset.filter(phone=filters['phone'])
            return queryset

        # Фильтрация для длительной аренды
        if deal_type == 'rent' and type_of_property == 'residential':
            queryset = RentLongAdvertisement.objects.all()
            queryset = apply_filters(queryset)
            serializer = RentLongAdvertisementSerializer(queryset, many=True)
            results.append({'RentLong': serializer.data})

        # Фильтрация для посуточной аренды
        elif deal_type == 'rent' and type_of_property == 'day':
            queryset = RentDayAdvertisement.objects.all()
            queryset = apply_filters(queryset)
            serializer = RentDayAdvertisementSerializer(queryset, many=True)
            results.append({'RentDay': serializer.data})

        # Фильтрация для продажи коммерческой недвижимости
        elif deal_type == 'sale' and type_of_property == 'commercial':
            queryset = SaleCommercialAdvertisement.objects.all()
            queryset = apply_filters(queryset)
            serializer = SaleCommercialAdvertisementSerializer(queryset, many=True)
            results.append({'SaleCommercial': serializer.data})

        # Фильтрация для аренды коммерческой недвижимости
        elif deal_type == 'rent' and type_of_property == 'commercial':
            queryset = RentCommercialAdvertisement.objects.all()
            queryset = apply_filters(queryset)
            serializer = RentCommercialAdvertisementSerializer(queryset, many=True)
            results.append({'RentCommercial': serializer.data})

        # Фильтрация для продажи жилой недвижимости
        elif deal_type == 'sale' and type_of_property == 'residential':
            queryset = SaleResidential.objects.all()
            queryset = apply_filters(queryset)
            serializer = SaleResidentialSerializer(queryset, many=True)
            results.append({'SaleResidential': serializer.data})

        return Response(results)