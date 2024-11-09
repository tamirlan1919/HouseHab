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
    min_price = django_filters.NumberFilter(field_name='rent_per_month', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='rent_per_month', lookup_expr='lte')

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

    subway_minute = django_filters.NumberFilter(field_name='minutesBusStop')
    min_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='lte')

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

    amenities = django_filters.MultipleChoiceFilter(
        method='filter_amenities',
        label='Amenities',
        choices=[
            ('conditioner', 'Кондиционер'),
            ('fridge', 'Холодильник'),
            ('tv', 'Телевизор'),
            ('dishwasher', 'Посудомоечная машина'),
            ('washingmMachine', 'Стиральная машина'),
            ('internet', 'Интернет'),
            ('phone', 'Телефон'),
            ('noFurniture', 'Без мебели'),
            ('inKitchen', 'На кухне'),
            ('inRooms', 'В комнатах')
        ]
    )

    rentalTerm = django_filters.MultipleChoiceFilter(
        field_name='rentalTerm',
        choices=[
            ('several_months', 'Несколько месяцев'),
            ('year', 'От года')
        ]
    )

    livingConditions = django_filters.MultipleChoiceFilter(
        field_name='livingConditions',
        choices=[
            ('allowed_with_children', 'Можно с детьми'),
            ('allowed_with_pets', 'Можно с животными')
        ]
    )

    repair = django_filters.MultipleChoiceFilter(
        field_name='repair',
        choices=[
            ('unrepaired', 'Без ремонта'),
            ('cosmetic', 'Косметический'),
            ('euro', 'Евро'),
            ('designer', 'Дизайнерский')
        ]
    )

    min_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='gte', label='Floor From')
    max_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='lte', label='Floor To')
    min_floor_in_house = django_filters.NumberFilter(field_name='floorsHouse', lookup_expr='gte', label='Мин этажей')
    max_floor_in_house = django_filters.NumberFilter(field_name='floorsHouse', lookup_expr='lte', label='Макс этажей')

    not_first = django_filters.BooleanFilter(method='filter_not_first', label='Not First Floor')
    not_last = django_filters.BooleanFilter(method='filter_not_last', label='Not Last Floor')
    only_last = django_filters.BooleanFilter(method='filter_only_last', label='Only Last Floor')
    penthouse = django_filters.BooleanFilter(method='filter_penthouse', label='Penthouse')

    propertyType = django_filters.MultipleChoiceFilter(
        field_name='propertyType',
        choices=[
            ('flat', 'Квартира'),
            ('apartments', 'Апартаменты')
        ]
    )

    is_freightElevator = django_filters.BooleanFilter(field_name='freightElevator', label='Грузовой лифт')
    is_passengerElevator = django_filters.BooleanFilter(field_name='passengerElevator', label='Пассажирский лифт')
    no_deposit = django_filters.BooleanFilter(method='filter_no_deposit', label='Без залога')

    def filter_not_first(self, queryset, name, value):
        if value:
            return queryset.exclude(floor=1)
        return queryset

    def filter_not_last(self, queryset, name, value):
        max_floor = 20  # Замените на актуальный максимальный этаж, если доступен динамически
        if value:
            return queryset.exclude(floor=max_floor)
        return queryset

    def filter_only_last(self, queryset, name, value):
        max_floor = 20  # Замените на актуальный максимальный этаж, если доступен динамически
        if value:
            return queryset.filter(floor=max_floor)
        return queryset

    def filter_penthouse(self, queryset, name, value):
        penthouse_floor = 20  # Настройте это значение в зависимости от ваших требований
        if value:
            return queryset.filter(floor=penthouse_floor)
        return queryset

    def filter_amenities(self, queryset, name, value):
        if value:
            query = Q()
            for item in value:
                query |= Q(apartment__contains=item) | Q(connection__contains=item) | Q(furniture__contains=item)
            return queryset.filter(query)
        return queryset

    def filter_bathroom_type(self, queryset, name, value):
        if value == 'combined':
            return queryset.filter(combinedBathroom=True)
        elif value == 'separate':
            return queryset.filter(separateBathroom=True)
        return queryset

    def filter_no_deposit(self, queryset, name, value):
        if value:
            return queryset.filter(Q(deposit=0) | Q(deposit__isnull=True))
        return queryset

    class Meta:
        model = RentLongAdvertisement
        fields = [
            'min_price', 'max_price', 'obj', 'roomsNumber', 'address', 'fromOwner', 'pathType',
            'subway_minute', 'min_totalArea', 'max_totalArea',
            'balcony', 'loggia', 'ceilingHeight', 'bathroom', 'amenities', 'rentalTerm',
            'livingConditions', 'repair', 'min_floor', 'max_floor', 'min_floor_in_house',
            'max_floor_in_house', 'not_first', 'not_last', 'only_last', 'penthouse',
            'propertyType', 'is_freightElevator', 'is_passengerElevator', 'no_deposit'

        ]


class RentDailyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='daily_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='daily_price', lookup_expr='lte')
    obj = django_filters.MultipleChoiceFilter(
        field_name='obj',
        choices=[
            ('flat', 'Квартира'),
            ('room', 'Комната'),
            ('house', 'Дом'),
            ('place', 'Койко-место')
        ]
    )
    roomsNumber = ArrayFilter(field_name='roomsNumber')
    min_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='lte')
    fromOwner = django_filters.BooleanFilter(field_name='accountType', label='От собственника')
    pathType = django_filters.MultipleChoiceFilter(
        field_name='pathType',
        choices=[
            ('foot', 'Пешком'),
            ('transport', 'Транспорт')
        ]
    )
    subway_minute = django_filters.NumberFilter(field_name='minutesBusStop', lookup_expr='gte')
    min_kitchenArea = django_filters.NumberFilter(field_name='kitchenArea', lookup_expr='gte')
    max_kitchenArea = django_filters.NumberFilter(field_name='kitchenArea', lookup_expr='lte')
    livingConditions = django_filters.MultipleChoiceFilter(
        field_name='livingConditions',
        choices=[
            ('allowed_with_children', 'Можно с детьми'),
            ('allowed_with_pets', 'Можно с животными')
        ]
    )

    amenities = django_filters.MultipleChoiceFilter(
        method='filter_amenities',
        label='Amenities',
        choices=[
            ('conditioner', 'Кондиционер'),
            ('fridge', 'Холодильник'),
            ('tv', 'Телевизор'),
            ('dishwasher', 'Посудомоечная машина'),
            ('washingmMachine', 'Стиральная машина'),
            ('internet', 'Интернет'),
            ('phone', 'Телефон'),
            ('noFurniture', 'Без мебели'),
            ('inKitchen', 'На кухне'),
            ('inRooms', 'В комнатах')
        ]
    )

    min_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='gte', label='Floor From')
    max_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='lte', label='Floor To')
    min_floor_in_house = django_filters.NumberFilter(field_name='floorsHouse', lookup_expr='gte', label='Мин этажей')
    max_floor_in_house = django_filters.NumberFilter(field_name='floorsHouse', lookup_expr='lte', label='Макс этажей')

    not_first = django_filters.BooleanFilter(method='filter_not_first', label='Not First Floor')
    not_last = django_filters.BooleanFilter(method='filter_not_last', label='Not Last Floor')
    only_last = django_filters.BooleanFilter(method='filter_only_last', label='Only Last Floor')
    penthouse = django_filters.BooleanFilter(method='filter_penthouse', label='Penthouse')

    propertyType = django_filters.MultipleChoiceFilter(
        field_name='propertyType',
        choices=[
            ('flat', 'Квартира'),
            ('apartments', 'Апартаменты')
        ]
    )

    no_deposit = django_filters.BooleanFilter(method='filter_no_deposit', label='Без залога')

    def filter_no_deposit(self, queryset, name, value):
        if value:
            return queryset.filter(Q(deposit=0) | Q(deposit__isnull=True))
        return queryset

    def filter_not_first(self, queryset, name, value):
        if value:
            return queryset.exclude(floor=1)
        return queryset

    def filter_not_last(self, queryset, name, value):
        max_floor = 20  # Замените на актуальный максимальный этаж, если доступен динамически
        if value:
            return queryset.exclude(floor=max_floor)
        return queryset

    def filter_only_last(self, queryset, name, value):
        max_floor = 20  # Замените на актуальный максимальный этаж, если доступен динамически
        if value:
            return queryset.filter(floor=max_floor)
        return queryset

    def filter_penthouse(self, queryset, name, value):
        penthouse_floor = 20  # Настройте это значение в зависимости от ваших требований
        if value:
            return queryset.filter(floor=penthouse_floor)
        return queryset

    def filter_amenities(self, queryset, name, value):
        if value:
            query = Q()
            for item in value:
                query |= Q(apartment__contains=item) | Q(connection__contains=item) | Q(furniture__contains=item)
            return queryset.filter(query)
        return queryset

    class Meta:
        model = RentDayAdvertisement
        fields = [
                    'min_price', 'max_price', 'obj', 'roomsNumber', 'min_totalArea', 'max_totalArea',
                    'fromOwner', 'pathType', 'subway_minute', 'min_kitchenArea', 'max_kitchenArea',
                    'livingConditions', 'amenities', 'min_floor', 'max_floor', 'min_floor_in_house',
                    'max_floor_in_house', 'not_first', 'not_last', 'only_last', 'penthouse',
                    'propertyType', 'no_deposit'
                ]



class RentCommercialFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(method='filter_by_price_range', label='Min Price')
    max_price = django_filters.NumberFilter(method='filter_by_price_range', label='Max Price')
    is_total = django_filters.BooleanFilter(field_name='currency_rent_month')
    is_per_month = django_filters.BooleanFilter(field_name='currency_rent_month_per_m2')
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
    subway_minute = django_filters.NumberFilter(field_name='minutesBusStop', lookup_expr='gte')

    min_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='gte')
    max_totalArea = django_filters.NumberFilter(field_name='totalArea', lookup_expr='lte')

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

    def filter_by_price_range(self, queryset, name, value):
        if name == 'min_price':
            return queryset.filter(
                Q(rent_per_month__gte=value) | Q(rent_per_month_per_m2__gte=value)
            )
        if name == 'max_price':
            return queryset.filter(
                Q(rent_per_month__lte=value) | Q(rent_per_month_per_m2__lte=value)
            )
        return queryset

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

    min_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='gte', label='Floor From')
    max_floor = django_filters.NumberFilter(field_name='floor', lookup_expr='lte', label='Floor To')
    min_floor_in_house = django_filters.NumberFilter(field_name='floorsHouse', lookup_expr='gte', label='Мин этажей')
    max_floor_in_house = django_filters.NumberFilter(field_name='floorsHouse', lookup_expr='lte', label='Макс этажей')

    not_first = django_filters.BooleanFilter(method='filter_not_first', label='Not First Floor')
    not_last = django_filters.BooleanFilter(method='filter_not_last', label='Not Last Floor')
    only_last = django_filters.BooleanFilter(method='filter_only_last', label='Only Last Floor')
    penthouse = django_filters.BooleanFilter(method='filter_penthouse', label='Penthouse')
    year_built_min = django_filters.NumberFilter(field_name='yearBuilt', lookup_expr='gte')
    year_built_max = django_filters.NumberFilter(field_name='yearBuilt', lookup_expr='lte')
    # Filter for 'Без залога' (Without Deposit)
    no_deposit = django_filters.BooleanFilter(
        field_name='security_deposit',
        method='filter_no_deposit',
        label='Без залога'
    )

    # Filter for 'Без комиссии' (Without Commission)
    no_commission = django_filters.BooleanFilter(
        field_name='agentBonus',
        method='filter_no_commission',
        label='Без комиссии'
    )
    def filter_not_first(self, queryset, name, value):
        if value:
            return queryset.exclude(floor=1)
        return queryset

    def filter_not_last(self, queryset, name, value):
        max_floor = 20  # Замените на актуальный максимальный этаж, если доступен динамически
        if value:
            return queryset.exclude(floor=max_floor)
        return queryset

    def filter_only_last(self, queryset, name, value):
        max_floor = 20  # Замените на актуальный максимальный этаж, если доступен динамически
        if value:
            return queryset.filter(floor=max_floor)
        return queryset

    def filter_penthouse(self, queryset, name, value):
        penthouse_floor = 20  # Настройте это значение в зависимости от ваших требований
        if value:
            return queryset.filter(floor=penthouse_floor)
        return queryset

    def filter_no_deposit(self, queryset, name, value):
        if value:  # If True, filter for zero or empty deposit
            return queryset.filter(security_deposit__isnull=True) | queryset.filter(security_deposit=0)
        return queryset

    def filter_no_commission(self, queryset, name, value):
        if value:  # If True, filter for no agent commission
            return queryset.filter(agentBonus='Нет')
        return queryset

    class Meta:
        model = RentCommercialAdvertisement
        fields = [
            'min_price', 'max_price', 'is_total', 'is_per_month', 'obj', 'address',
            'fromOwner', 'pathType', 'subway_minute', 'min_totalArea', 'max_totalArea',
            'ceilingHeight', 'bathroom', 'balcony', 'loggia', 'planning', 'min_floor',
            'max_floor', 'min_floor_in_house', 'max_floor_in_house', 'not_first',
            'not_last', 'only_last', 'penthouse', 'year_built_min', 'year_built_max',
            'no_deposit', 'no_commission'
        ]
