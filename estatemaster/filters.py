import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from .models import *

class ArrayFilter(filters.BaseCSVFilter, filters.CharFilter):
    def filter(self, qs, value):
        if value:
            if isinstance(value, list):
                cleaned_value = ','.join(value)
            else:
                cleaned_value = value
            cleaned_value = cleaned_value.replace('[', '').replace(']', '')
            values = [v.strip() for v in cleaned_value.split(',')]
            return qs.filter(**{f"{self.field_name}__in": values})
        return qs


class ArrayMinFilter(filters.BaseCSVFilter, filters.CharFilter):
    def filter(self, qs, value):
        if value:
            if isinstance(value, list):
                cleaned_value = ','.join(value)
            else:
                cleaned_value = value
            cleaned_value = cleaned_value.replace('[', '').replace(']', '')

            # Convert values to a list of floats and get the minimum
            values = [float(v.strip()) for v in cleaned_value.split(',') if v.strip()]
            if values:
                min_value = min(values)
                return qs.filter(**{f"{self.field_name}__gte": min_value})
        return qs

class SaleResidentialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    roomsNumber = ArrayFilter(field_name='roomsNumber')

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
    fromOwner = django_filters.BooleanFilter(field_name='accountType', label='От собственника')
    pathType = django_filters.MultipleChoiceFilter(
        field_name='pathType',
        choices=[
            ('foot', 'Пешком'),
            ('transport', 'Транспорт')
        ]
    )
    min_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')
    min_livingArea = django_filters.NumberFilter(field_name='livingArea', lookup_expr='gte')
    max_livingArea = django_filters.NumberFilter(field_name='livingArea', lookup_expr='gte')
    min_kitchenArea = django_filters.NumberFilter(field_name='kitchenArea', lookup_expr='gte')
    max_kitchenArea = django_filters.NumberFilter(field_name='kitchenArea', lookup_expr='gte')

    # Boolean filters for balcony and loggia
    balcony = django_filters.BooleanFilter(field_name='balconies', label='Balcony Exists')
    loggia = django_filters.BooleanFilter(field_name='loggia', label='Loggia Exists')

    # Multi-select for ceilingHeight
    ceilingHeight = django_filters.NumberFilter(field_name='ceilingHeight', lookup_expr='gte',
                                                label='Minimum Ceiling Height')

    # Boolean filters for bathroom and combinedBathroom

    # Bathroom choice
    bathroom = django_filters.ChoiceFilter(
        method='filter_bathroom_type',
        choices=[
            ('combined', 'Combined Bathroom'),
            ('separate', 'Separate Bathroom')
        ],
        label='Bathroom Type'
    )

    def filter_bathroom_type(self, queryset, name, value):
        if value == 'combined':
            return queryset.filter(combinedBathroom=True)
        elif value == 'separate':
            return queryset.filter(separateBathroom=True)
        return queryset

    class Meta:
        model = SaleResidential
        fields = [
            'obj', 'address', 'roomsNumber', 'max_price', 'min_price', 'fromOwner', 'pathType',
            'min_totalArea', 'max_totalArea', 'min_livingArea', 'max_livingArea',
            'min_kitchenArea', 'max_kitchenArea', 'ceilingHeight', 'balcony', 'loggia',
            'bathroom'
        ]

class SaleCommercialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(method='filter_by_price_range', label='Min Price')
    max_price = django_filters.NumberFilter(method='filter_by_price_range', label='Max Price')
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
    fromOwner = django_filters.BooleanFilter(field_name='accountType', label='От собственника')
    pathType = django_filters.MultipleChoiceFilter(
        field_name='pathType',
        choices=[
            ('foot', 'Пешком'),
            ('transport', 'Транспорт')
        ]
    )
    min_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')

    # Multi-select for ceilingHeight
    ceilingHeight = django_filters.NumberFilter(field_name='ceilingHeight', lookup_expr='gte',
                                                label='Minimum Ceiling Height')
    # Boolean filters for bathroom and combined
    bathroom = django_filters.ChoiceFilter(
        method='filter_bathroom_type',
        choices=[
            ('combined', 'Combined Bathroom'),
            ('separate', 'Separate Bathroom')
        ],
        label='Bathroom Type'
    )

    def filter_bathroom_type(self, queryset, name, value):
        if value == 'combined':
            return queryset.filter(combinedBathroom=True)
        elif value == 'separate':
            return queryset.filter(separateBathroom=True)
        return queryset

    planning = django_filters.MultipleChoiceFilter(
        field_name='planning',
        choices=[
            ('open', 'Открытая'),
            ('corridor', 'Коридор'),
            ('cabinet', 'Кабинетная')
        ])

    class Meta:
        model = SaleCommercialAdvertisement
        fields = [
            'obj', 'address', 'max_price', 'min_price', 'fromOwner', 'pathType',
            'min_totalArea', 'max_totalArea', 'ceilingHeight', 'bathroom',  'planning'
        ]

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
    roomsNumber = ArrayFilter(field_name='roomsNumber')
    address = django_filters.CharFilter(field_name='address')
    fromOwner = django_filters.BooleanFilter(field_name='accountType', label='От собственника')
    pathType = django_filters.MultipleChoiceFilter(
        field_name='pathType',
        choices=[
            ('foot', 'Пешком'),
            ('transport', 'Транспорт')
        ]
    )
    min_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')

    # Boolean filters for balcony and loggia
    balcony = django_filters.BooleanFilter(field_name='balconies', label='Balcony Exists')
    loggia = django_filters.BooleanFilter(field_name='loggia', label='Loggia Exists')

    # Multi-select for ceilingHeight
    ceilingHeight = django_filters.NumberFilter(field_name='ceilingHeight', lookup_expr='gte',
                                                label='Minimum Ceiling Height')
    # Boolean filters for bathroom and combined
    bathroom = django_filters.ChoiceFilter(
        method='filter_bathroom_type',
        choices=[
            ('combined', 'Combined Bathroom'),
            ('separate', 'Separate Bathroom')
        ],
        label='Bathroom Type'
    )

    def filter_bathroom_type(self, queryset, name, value):
        if value == 'combined':
            return queryset.filter(combinedBathroom=True)
        elif value == 'separate':
            return queryset.filter(separateBathroom=True)
        return queryset

    class Meta:
        model = RentLongAdvertisement
        fields = [
            'obj', 'address', 'roomsNumber', 'max_price', 'min_price', 'fromOwner', 'pathType',
            'min_totalArea', 'max_totalArea', 'ceilingHeight', 'balcony', 'loggia',
            'bathroom'
        ]

class RentCommercialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
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
    roomsNumber = ArrayFilter(field_name='roomsNumber')
    address = django_filters.CharFilter(field_name='address')
    fromOwner = django_filters.BooleanFilter(field_name='accountType', label='От собственника')
    pathType = django_filters.MultipleChoiceFilter(
        field_name='pathType',
        choices=[
            ('foot', 'Пешком'),
            ('transport', 'Транспорт')
        ]
    )
    min_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')

    # Multi-select for ceilingHeight
    ceilingHeight = django_filters.NumberFilter(field_name='ceilingHeight', lookup_expr='gte',
                                                label='Minimum Ceiling Height')
    # Boolean filters for bathroom and combined
    bathroom = django_filters.ChoiceFilter(
        method='filter_bathroom_type',
        choices=[
            ('combined', 'Combined Bathroom'),
            ('separate', 'Separate Bathroom')
        ],
        label='Bathroom Type'
    )

    def filter_bathroom_type(self, queryset, name, value):
        if value == 'combined':
            return queryset.filter(combinedBathroom=True)
        elif value == 'separate':
            return queryset.filter(separateBathroom=True)
        return queryset

    # Boolean filters for balcony and loggia
    balcony = django_filters.BooleanFilter(field_name='balconies', label='Balcony Exists')
    loggia = django_filters.BooleanFilter(field_name='loggia', label='Loggia Exists')

    planning = django_filters.MultipleChoiceFilter(
        field_name='planning',
        choices=[
            ('open', 'Открытая'),
            ('corridor', 'Коридор'),
            ('cabinet', 'Кабинетная')
        ])

    class Meta:
        model = RentCommercialAdvertisement
        fields = [
            'obj', 'address', 'roomsNumber', 'max_price', 'min_price', 'fromOwner', 'pathType',
            'min_totalArea', 'max_totalArea', 'ceilingHeight', 'bathroom',
            'balcony', 'loggia', 'planning'
        ]
