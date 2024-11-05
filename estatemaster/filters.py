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
    subway_minute = django_filters.NumberFilter(field_name='minutesBusStop', lookup_expr='gte')

    propertyType = django_filters.MultipleChoiceFilter(
        field_name='propertyType',
        choices=[
            ('flat', 'Квартира'),
            ('apartments', 'Апартаменты')
        ]
    )

    houseType = django_filters.MultipleChoiceFilter(
        field_name='houseType',
        choices=[
            ('brick', 'Кирпичный'),
            ('monolithic', 'Монолитный'),
            ('panel', 'Панельный'),
            ('block', 'Блочный'),
            ('wooden', 'Деревянный')
        ]
    )

    year_built_min = django_filters.NumberFilter(field_name='yearBuilt', lookup_expr='gte')
    year_built_max = django_filters.NumberFilter(field_name='yearBuilt', lookup_expr='lte')

    min_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='gte', label='Floor From')
    max_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='lte', label='Floor To')

    not_first = django_filters.BooleanFilter(method='filter_not_first', label='Not First Floor')
    not_last = django_filters.BooleanFilter(method='filter_not_last', label='Not Last Floor')
    only_last = django_filters.BooleanFilter(method='filter_only_last', label='Only Last Floor')
    penthouse = django_filters.BooleanFilter(method='filter_penthouse', label='Penthouse')

    def filter_not_first(self, queryset, name, value):
        if value:
            return queryset.exclude(floor=1)  # Exclude first floor
        return queryset

    def filter_not_last(self, queryset, name, value):
        max_floor = 20  # Replace with actual max floor if dynamically available
        if value:
            return queryset.exclude(floor=max_floor)  # Exclude last floor
        return queryset

    def filter_only_last(self, queryset, name, value):
        max_floor = 20  # Replace with actual max floor if dynamically available
        if value:
            return queryset.filter(floor=max_floor)  # Only last floor
        return queryset

    def filter_penthouse(self, queryset, name, value):
        penthouse_floor = 20  # Adjust this as per your criteria
        if value:
            return queryset.filter(floor=penthouse_floor)  # Filter for penthouse floor
        return queryset

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
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='lte')
    min_livingArea = django_filters.NumberFilter(field_name='livingArea', lookup_expr='gte')
    max_livingArea = django_filters.NumberFilter(field_name='livingArea', lookup_expr='lte')
    min_kitchenArea = django_filters.NumberFilter(field_name='kitchenArea', lookup_expr='gte')
    max_kitchenArea = django_filters.NumberFilter(field_name='kitchenArea', lookup_expr='lte')

    balcony = django_filters.BooleanFilter(field_name='balconies', label='Balcony Exists')
    loggia = django_filters.BooleanFilter(field_name='loggia', label='Loggia Exists')

    ceilingHeight = django_filters.NumberFilter(field_name='ceilingHeight', lookup_expr='gte',
                                                label='Minimum Ceiling Height')

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
            'min_price', 'max_price', 'roomsNumber', 'subway_minute', 'propertyType',
            'houseType', 'year_built_min', 'year_built_max', 'min_floor', 'max_floor',
            'not_first', 'not_last', 'only_last', 'penthouse', 'obj', 'address',
            'fromOwner', 'pathType', 'min_totalArea', 'max_totalArea', 'min_livingArea',
            'max_livingArea', 'min_kitchenArea', 'max_kitchenArea', 'balcony', 'loggia',
            'ceilingHeight', 'bathroom'
        ]


class SaleCommercialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(method='filter_by_price_range', label='Min Price')
    max_price = django_filters.NumberFilter(method='filter_by_price_range', label='Max Price')
    is_total = django_filters.BooleanFilter(field_name='currency_total')
    is_per_month = django_filters.BooleanFilter(field_name='currency_per')
    subway_minute = django_filters.NumberFilter(field_name='minutesBusStop')

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
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='lte')

    ceilingHeight = django_filters.NumberFilter(field_name='ceilingHeight', lookup_expr='gte',
                                                label='Minimum Ceiling Height')

    bathroom = django_filters.ChoiceFilter(
        method='filter_bathroom_type',
        choices=[
            ('combined', 'Combined Bathroom'),
            ('separate', 'Separate Bathroom')
        ],
        label='Bathroom Type'
    )

    planning = django_filters.MultipleChoiceFilter(
        field_name='planning',
        choices=[
            ('open', 'Открытая'),
            ('corridor', 'Коридор'),
            ('cabinet', 'Кабинетная')
        ]
    )

    min_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='gte', label='Floor From')
    max_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='lte', label='Floor To')

    not_first = django_filters.BooleanFilter(method='filter_not_first', label='Not First Floor')
    not_last = django_filters.BooleanFilter(method='filter_not_last', label='Not Last Floor')
    only_last = django_filters.BooleanFilter(method='filter_only_last', label='Only Last Floor')
    penthouse = django_filters.BooleanFilter(method='filter_penthouse', label='Penthouse')

    year_built_min = django_filters.NumberFilter(field_name='yearBuilt', lookup_expr='gte')
    year_built_max = django_filters.NumberFilter(field_name='yearBuilt', lookup_expr='lte')

    def filter_not_first(self, queryset, name, value):
        if value:
            return queryset.exclude(floor=1)  # Exclude first floor
        return queryset

    def filter_not_last(self, queryset, name, value):
        max_floor = 20  # Replace with actual max floor if dynamically available
        if value:
            return queryset.exclude(floor=max_floor)  # Exclude last floor
        return queryset

    def filter_only_last(self, queryset, name, value):
        max_floor = 20  # Replace with actual max floor if dynamically available
        if value:
            return queryset.filter(floor=max_floor)  # Only last floor
        return queryset

    def filter_penthouse(self, queryset, name, value):
        penthouse_floor = 20  # Adjust this as per your criteria
        if value:
            return queryset.filter(floor=penthouse_floor)  # Filter for penthouse floor
        return queryset

    def filter_bathroom_type(self, queryset, name, value):
        if value == 'combined':
            return queryset.filter(combinedBathroom=True)
        elif value == 'separate':
            return queryset.filter(separateBathroom=True)
        return queryset

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

    class Meta:
        model = SaleCommercialAdvertisement
        fields = [
            'min_price', 'max_price', 'is_total', 'is_per_month', 'subway_minute', 'obj',
            'address', 'fromOwner', 'pathType', 'min_totalArea', 'max_totalArea',
            'ceilingHeight', 'bathroom', 'planning', 'min_floor', 'max_floor',
            'not_first', 'not_last', 'only_last', 'penthouse', 'year_built_min',
            'year_built_max'
        ]

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
