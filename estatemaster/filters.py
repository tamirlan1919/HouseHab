import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from .models import *


class ArrayFilter(filters.BaseCSVFilter, filters.CharFilter):
    def filter(self, qs, value):
        if value:
            if isinstance(value, list):
                # If value is a list, combine it into a single string
                cleaned_value = ','.join(value)
            else:
                cleaned_value = value
            # Remove any brackets from the string
            cleaned_value = cleaned_value.replace('[', '').replace(']', '')
            # Split the string into individual values
            values = [v.strip() for v in cleaned_value.split(',')]
            return qs.filter(**{f"{self.field_name}__in": values})
        return qs


class SaleResidentialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Используем кастомный ArrayFilter
    roomsNumber = ArrayFilter(
        field_name='roomsNumber',

    )

    obj = django_filters.MultipleChoiceFilter(
        field_name='obj',
        choices=[
            ('flat', 'Квартира'),
            ('flatNewBuilding', 'Квартира в новостройке'),
            ('room', 'Комната'),
            ('flatShare', 'Доля в квартире'),
            ('house', 'Дом'),
            ('cottage', 'Коттедж'),
            ('tanhouse', 'Таунхаус'),
            ('partHouse', 'Часть дома'),
            ('plot', 'Участок')
        ]
    )

    address = django_filters.CharFilter(field_name='address')

    class Meta:
        model = SaleResidential
        fields = ['obj', 'address', 'roomsNumber', 'max_price', 'min_price']


class SaleCommercialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(method='filter_by_price_range', label='Min Price')
    max_price = django_filters.NumberFilter(method='filter_by_price_range', label='Max Price')

    # MultipleChoiceFilter для количества комнат

    # MultipleChoiceFilter для выбора объектов
    obj = django_filters.MultipleChoiceFilter(
        field_name='obj',
        choices=[
            ('office', 'Офис'),
            ('building', 'Здание'),
            ('retail_space', 'Торговая площадь'),
            ('free_place', 'Помещение свободного назначения'),
            ('production', 'Производство'),
            ('warehouse', 'Склад'),
            ('garage', 'Гараж'),
            ('business', 'Бизнес'),
            ('commercial_land', 'Коммерческая земля')
        ]
    )

    address = django_filters.CharFilter(field_name='address')

    class Meta:
        model = SaleCommercialAdvertisement
        fields = ['obj', 'address', 'max_price', 'min_price']

    def filter_by_price_range(self, queryset, name, value):
        if name == 'min_price':
            return queryset.filter(
                Q(total_price__gte=value) | Q(price_per_m2__gte=value)
            )
        if name == 'max_price':
            return queryset.filter(
                Q(total_price__lte=value) | Q(price_per_m2__lte=value)
            )
        return queryset

class RentLongFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Фильтр по объекту с множественным выбором
    obj = django_filters.MultipleChoiceFilter(
        field_name='obj',
        choices=[
            ('flat', 'Квартира'),
            ('flatNewBuilding', 'Квартира в новостройке'),
            ('room', 'Комната'),
            ('flatShare', 'Доля в квартире'),
            ('house', 'Дом'),
            ('cottage', 'Коттедж'),
            ('tanhouse', 'Таунхаус'),
            ('partHouse', 'Часть дома'),
            ('plot', 'Участок')
        ]
    )

    # Фильтр по количеству комнат с множественным выбором
    roomsNumber = ArrayFilter(
        field_name='roomsNumber'

    )

    address = django_filters.CharFilter(field_name='address')

    class Meta:
        model = RentLongAdvertisement
        fields = ['obj', 'address', 'roomsNumber', 'max_price', 'min_price']


class RentCommercialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Фильтр по объекту с множественным выбором
    obj = django_filters.MultipleChoiceFilter(
        field_name='obj',
        choices=[
            ('office', 'Офис'),
            ('building', 'Здание'),
            ('retail_space', 'Торговая площадь'),
            ('free_place', 'Помещение свободного назначения'),
            ('production', 'Производство'),
            ('warehouse', 'Склад'),
            ('garage', 'Гараж'),
            ('business', 'Бизнес'),
            ('commercial_land', 'Коммерческая земля')
        ]
    )

    # Фильтр по количеству комнат с множественным выбором
    roomsNumber = ArrayFilter(
        field_name='roomsNumber'

    )

    address = django_filters.CharFilter(field_name='address')

    class Meta:
        model = RentCommercialAdvertisement
        fields = ['obj', 'address', 'roomsNumber', 'max_price', 'min_price']