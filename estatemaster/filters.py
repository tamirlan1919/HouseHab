import django_filters
from .models import *

from django_filters import rest_framework as filters
class ListFilter(filters.BaseCSVFilter, filters.CharFilter):
    """
    Фильтр для работы с запросами вида roomsNumber=[1,2,3]
    Преобразует строку в список значений.
    """
    def filter(self, qs, value):
        if value:
            value = value.strip('[]').split(',')  # Убираем квадратные скобки и разделяем по запятым
        return super().filter(qs, value)

class SaleResidentialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    roomsNumber = ListFilter(
        field_name='roomsNumber',
        choices = [
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
    obj = ListFilter(
        field_name= 'obj',
        choices = [
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
    roomsNumber = ListFilter(
        field_name='roomsNumber',
        choices = [
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
    obj = ListFilter(
        field_name= 'obj',
        choices = [
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
    obj = ListFilter(
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
    roomsNumber = ListFilter(
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

    class Meta:
        model = RentLongAdvertisement
        fields = ['obj', 'address', 'roomsNumber', 'max_price', 'min_price']


class RentCommercialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    obj = ListFilter(
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
    roomsNumber = ListFilter(
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

    class Meta:
        model = RentCommercialAdvertisement
        fields = ['obj', 'address', 'roomsNumber', 'max_price', 'min_price']
