import django_filters
from django_filters import rest_framework as filters
from .models import *


class ArrayFilter(filters.BaseCSVFilter, filters.CharFilter):
    """
    Фильтр для работы с запросами вида roomsNumber=[1,2]
    Преобразует строку в список значений.
    """
    def filter(self, qs, value):
        if value:
            # Убираем квадратные скобки и разделяем строку по запятым
            value = value.strip('[]').split(',')
        return super().filter(qs, value)

class SaleResidentialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Используем MultipleChoiceFilter для множественного выбора комнат
    roomsNumber = django_filters.MultipleChoiceFilter(
        field_name='roomsNumber',
        choices=[
            ('studio', 'Студия'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('overSix', '6'),
            ('freePlanning', 'Свободная планировка')
        ]
    )

    # Для obj также используем MultipleChoiceFilter
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
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # MultipleChoiceFilter для количества комнат
    roomsNumber = django_filters.MultipleChoiceFilter(
        field_name='roomsNumber',
        choices=[
            ('studio', 'Студия'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('overSix', '6'),
            ('freePlanning', 'Свободная планировка')
        ]
    )

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
        fields = ['obj', 'address', 'roomsNumber', 'max_price', 'min_price']

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
    roomsNumber = django_filters.MultipleChoiceFilter(
        field_name='roomsNumber',
        choices=[
            ('studio', 'Студия'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('overSix', '6'),
            ('freePlanning', 'Свободная планировка')
        ]
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
    roomsNumber = django_filters.MultipleChoiceFilter(
        field_name='roomsNumber',
        choices=[
            ('studio', 'Студия'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('overSix', '6'),
            ('freePlanning', 'Свободная планировка')
        ]
    )

    address = django_filters.CharFilter(field_name='address')

    class Meta:
        model = RentCommercialAdvertisement
        fields = ['obj', 'address', 'roomsNumber', 'max_price', 'min_price']