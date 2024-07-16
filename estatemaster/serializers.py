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
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'username', 'photo', 'date_of_birth', 'account_type', 'is_confirm', 'professional_profile')

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