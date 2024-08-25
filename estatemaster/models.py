from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from .managers import CustomUserManager
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='uploaded_images')


    class Meta:
        verbose_name = 'Фотографии'
        verbose_name_plural = 'Фото'
    def __str__(self):
        return f"Image {self.id} - {self.owner.username}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    account_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('professional', 'Professional')], default='individual')
    photo = models.ImageField(upload_to='images/',blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_confirm = models.BooleanField(default=False,blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'account_type']
    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )


    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'





class ProfessionalProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='professional_profile')
    RENTAL_CHOICES = (
        ('жилая', 'Жилая'),
        ('загородная', 'Загородная'),
        ('зарубежная', 'Зарубежная'),
        ('коммерческая', 'Коммерческая'),
    )
    MORTGAGE_CHOICES = (
        ('ипотека', 'Ипотека'),
        ('рефинансирование', 'Рефинансирование'),
    )
    OTHER_SERVICES_CHOICES = (
        ('страхование', 'Страхование'),
        ('нотариат', 'Нотариат'),
        ('управление_объектами', 'Управление объектами'),
        ('строительство', 'Строительство'),
        ('консультация', 'Консультация'),
        ('дизайн_интерьера', 'Дизайн интерьера'),
        ('ремонт', 'Ремонт'),
        ('архитектура', 'Архитектура'),
    )
    SALE_CHOICES = (
        ('жилая', 'Жилая'),
        ('коммерческая', 'Коммерческая'),
        ('загородная', 'Загородная'),
        ('зарубежная', 'Зарубежная'),
    )
    ROLE_CHOICES = (
        ('realtor', 'Риелтор'),
        ('agency', 'Агентство'),
        ('developer', 'Застройщик'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='realtor')
    place_of_work = models.CharField(max_length=100, blank=True, null=True)
    bd = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    working_hours_start = models.TimeField(blank=True, null=True)
    working_hours_end = models.TimeField(blank=True, null=True)
    experience = models.PositiveIntegerField( blank=True, null=True)
    is_macler = models.BooleanField(blank=True,null=True)
    about_me = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True,null=True)
    about_company = models.CharField(max_length=100, blank=True,null=True)
    email = models.EmailField(max_length=255,blank=True,null=True)
    date_company = models.DateField(blank=True,null=True)
    how_houses = models.PositiveIntegerField(blank=True,null=True)
    how_houses_building = models.PositiveIntegerField(blank=True,null=True)
    count_zhk = models.PositiveIntegerField(blank=True,null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    # Добавляем специализации как булевы поля


    rental_types = models.CharField(max_length=255, blank=True,null=True,  choices=RENTAL_CHOICES)
    mortgage_types = models.CharField(max_length=255, blank=True,null=True,  choices=MORTGAGE_CHOICES)
    other_services = models.CharField(max_length=255, blank=True, null=True, choices=OTHER_SERVICES_CHOICES)
    sale_types = models.CharField(max_length=255, blank=True, null=True, choices=SALE_CHOICES)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Проф пользователь'
        verbose_name_plural = 'Проф пользователи'


class PromotionConfig(models.Model):
    promotion_type = models.CharField(
        max_length=20,
        choices=[
            ('standard', 'Стандарт'),
            ('premium', 'Премиум'),
            ('top', 'Топ'),
        ],
        unique=True
    )
    cost_per_day = models.PositiveIntegerField()
    discount_7_days = models.FloatField(default=0.10)
    discount_14_days = models.FloatField(default=0.15)
    discount_30_days = models.FloatField(default=0.20)

    def __str__(self):
        return self.get_promotion_type_display()

class Builder(models.Model):
    name = models.CharField(max_length=100,blank=True)
    zone = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=500,blank=True)

    class Meta:
        verbose_name = 'Застройщики'
        verbose_name_plural = 'Застройщик'

    def __str__(self):
        return self.name


class Promotion(models.Model):
    PROMOTION_TYPE_CHOICES = [
        ('standard', 'Стандарт'),
        ('premium', 'Премиум'),
        ('top', 'Топ'),
    ]

    DURATION_CHOICES = [
        (1, 'Посуточно'),
        (7, '7 дней'),
        (14, '14 дней'),
        (30, '30 дней'),
    ]

    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPE_CHOICES, default='standard')
    duration = models.PositiveIntegerField(choices=DURATION_CHOICES)
    config = models.ForeignKey(PromotionConfig, on_delete=models.CASCADE, null=True, blank=True)




    def calculate_total_cost(self):
        if not self.config:
            return 0

        base_cost = self.duration * self.config.cost_per_day
        discount = 0

        if self.duration == 7:
            discount = base_cost * self.config.discount_7_days
        elif self.duration == 14:
            discount = base_cost * self.config.discount_14_days
        elif self.duration == 30:
            discount = base_cost * self.config.discount_30_days

        return base_cost - discount

    def __str__(self):
        return f"{self.get_promotion_type_display()} - {self.duration} days"


class AdvertisementPhoto(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Ссылка на пользователя, загружающего фото
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    advertisement = GenericForeignKey('content_type', 'object_id')

    image = models.ImageField(upload_to='advertisement_photos/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Photo for {self.content_type} - {self.description or 'No Description'}"
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Если слаг пустой, то генерируем его из name
        if not self.slug:
            self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

class SaleResidential(models.Model):
    VIEW_CHOICES = [
        ('outside', 'На улицу'),
        ('courtyard', 'Во двор'),
        ('atSea', 'На море')
    ]
    APARTMENT_ENTRANCE_CHOICES = [
        ('ramp', 'Пандус'),
        ('trashChute', 'Мусоропровод')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner',blank=True)
    dealType = models.CharField(max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')],default='sale',blank=True)
    estateType = models.CharField(max_length=50, choices=[('residential', 'Жилая'), ('commercial','Коммерческая')],blank=True)
    obj = models.CharField(max_length=100, choices=[
        ('flat', 'Квартира'),
        ('flatNewBuilding', 'Квартира в новостройке'),
        ('room', 'Комната'),
        ('flatShare', 'Доля в квартире'),
        ('house', 'Дом'),
        ('cottage', 'Коттедж'),
        ('tanhouse', 'Таунхаус'),
        ('partHouse', 'Часть дома'),
        ('plot', 'Участок')
    ])
    region = models.OneToOneField(Location, on_delete=models.CASCADE,blank=True, null=True)
    address = models.CharField(max_length=400, null=True)
    nearestStop = models.CharField(max_length=400,null=True)
    minutesBusStop = models.PositiveIntegerField(blank=True)
    pathType = models.CharField(max_length=20, choices=[('foot', 'Пешком'), ('transport', 'Транспорт')], default='foot')
    floor = models.PositiveIntegerField()
    floorsHouse = models.PositiveIntegerField()
    flatNumber = models.PositiveIntegerField(blank=True)
    yaerBuilt = models.PositiveIntegerField(blank=True, null=True)
    ceilingHeight = models.FloatField(blank=True, null=True)
    houseType = models.CharField(max_length=100, choices=[
        ('brick', 'Кирпичный'),
        ('monolithic', 'Монолитный'),
        ('panel', 'Панельный'),
        ('block', 'Блочный'),
        ('wooden', 'Деревянный'),

    ],blank=True,null=True)
    roomsNumber = models.CharField(max_length=20, choices=[
        ('studio', 'Студия'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('overSix', '6'),
        ('freePlanning', 'Свободная планировка')
    ])
    totalArea = models.PositiveIntegerField()
    livingArea = models.PositiveIntegerField(blank=True, null=True)
    kitchenArea = models.PositiveIntegerField(blank=True, null=True)
    propertyType = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartments', 'Апартаменты')],blank=True)
    photos = GenericRelation(AdvertisementPhoto)
    youtubeLink = models.CharField(max_length=300, blank=True, null=True)

    balconies = models.PositiveIntegerField(default=0)
    loggia = models.PositiveIntegerField(default=0)
    viewFromWindow = models.CharField(max_length=10,choices=VIEW_CHOICES, blank=True, null=True)
    separateBathroom = models.PositiveIntegerField(default=0)
    repair = models.CharField(max_length=70, choices=[('unrepaired', 'Без ремонта'), ('cosmetic', 'Косметический'), ('euro', 'Евро'), ('designer', 'Дизайнерский')], blank=True, null=True)
    freightElevator = models.PositiveIntegerField(default=0)
    passengerElevator = models.PositiveIntegerField(default=0)
    combinedBathroom = models.PositiveIntegerField(default=0)
    apartmentEntrance = models.CharField(max_length=10 ,choices=APARTMENT_ENTRANCE_CHOICES, blank=True, null=True)
    parking = models.CharField(max_length=30, choices=[('ground', 'Наземная'), ('multiLevel', 'Многоуровневая'), ('underground', 'Подземная'), ('rooftop', 'На крыше')], blank=True, null=True)
    title = models.CharField(max_length=100, null=True)
    description = models.TextField()
    CURRENCY_CHOICES = [
        ('MZN', 'MZN'),
        ('USD', 'Доллар'),
        ('EUR', 'Евро'),
    ]
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')
    saleType = models.CharField(max_length=50, choices=[('onlySale', 'Только продаю'), ('buyingAnother', 'Одновременно покупаю другую')],blank=True)
    phone = models.CharField(max_length=30, null=True)
    whatsapp = models.CharField(max_length=300,null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True,null=True)
    class Meta:
        verbose_name = 'Жилые прожажи'
        verbose_name_plural = 'Жилая продажа'

    def __str__(self):
        return self.title





class RentLongAdvertisement(models.Model):
    VIEW_CHOICES = [
        ('outside', 'На улицу'),
        ('courtyard', 'Во двор'),
        ('atSea', 'На море')
    ]
    APARTMENT_ENTRANCE_CHOICES = [
        ('ramp', 'Пандус'),
        ('trashChute', 'Мусоропровод')
    ]
    BATHROOM_CHOICES = [
        ('bath', 'Ванна'),
        ('showerRoom', 'Душевая кабина')
    ]

    TECH_CHOICES = [
        ('conditioner', 'Кондиционер'),
        ('fridge', 'Холодильник'),
        ('tv', 'Телевизор'),
        ('dishwasher', 'Посудомоечная машина'),
        ('washingmMachine', 'Стиральная машина')
    ]

    COMMUNICATION_CHOICES = [
        ('internet', 'Интернет'),
        ('phone', 'Телефон')
    ]
    FURNITURE_CHOICES = [
        ('noFurniture', 'Без мебели'),
        ('inKitchen', 'На кухне'),
        ('inRooms', 'В комнатах')
    ]
    PREPAYMENT_CHOICES = [
        ('1_month', 'За 1 месяц'),
        ('2_months', '2 месяца'),
        ('3_months', '3 месяца'),
        ('4+_months', '4+')
    ]
    CURRENCY_CHOICES = [
        ('MZN', 'MZN'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]
    LIVING_CONDITIONS_CHOICES = [
        ('allowed_with_children', 'Можно с детьми'),
        ('allowed_with_pets', 'Можно с животными')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                   default='owner', blank=True)
    dealType = models.CharField(max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')], default='sale',
                                blank=True)
    estateType = models.CharField(max_length=50, choices=[('residential', 'Жилая'), ('commercial', 'Коммерческая')],
                                  blank=True)
    leaseType = models.CharField(max_length=70, choices=[('longTerm', 'Длительно'), ('daily', 'Посуточно')], blank=True)

    obj = models.CharField(max_length=100, choices=[
        ('flat', 'Квартира'),
        ('flatNewBuilding', 'Квартира в новостройке'),
        ('room', 'Комната'),
        ('flatShare', 'Доля в квартире'),
        ('house', 'Дом'),
        ('cottage', 'Коттедж'),
        ('tanhouse', 'Таунхаус'),
        ('partHouse', 'Часть дома'),
        ('plot', 'Участок')
    ])
    region = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=400, null=True)
    nearestStop = models.CharField(max_length=400,null=True)
    minutesBusStop = models.PositiveIntegerField(blank=True, null=True ,default=0)
    pathType = models.CharField(max_length=20, choices=[('foot', 'Пешком'), ('transport', 'Транспорт')],
                                default='foot')
    floor = models.PositiveIntegerField()
    floorsHouse = models.PositiveIntegerField()
    flatNumber = models.PositiveIntegerField(blank=True, default=0)
    roomsNumber = models.CharField(max_length=20, choices=[
        ('studio', 'Студия'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('overSix', '6'),
        ('freePlanning', 'Свободная планировка')
    ])

    totalArea = models.PositiveIntegerField(blank=True, default=0)
    livingArea = models.PositiveIntegerField(blank=True, null=True)
    kitchenArea = models.PositiveIntegerField(blank=True, null=True)
    propertyType = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartments', 'Апартаменты')])
    photos = GenericRelation(AdvertisementPhoto)
    youtubeLink = models.CharField(max_length=300, blank=True, null=True)
    viewFromWindow = models.CharField(max_length=10,choices=VIEW_CHOICES, blank=True, null=True)
    balconies = models.PositiveIntegerField(default=0)
    loggia = models.PositiveIntegerField(default=0)
    separateBathroom = models.PositiveIntegerField(default=0)
    combinedBathroom = models.PositiveIntegerField(default=0)
    repair = models.CharField(max_length=70, choices=[('unrepaired', 'Без ремонта'), ('cosmetic', 'Косметический'), ('euro', 'Евро'), ('designer', 'Дизайнерский')], blank=True, null=True)
    freightElevator = models.PositiveIntegerField(default=0)
    passengerElevator = models.PositiveIntegerField(default=0)
    apartmentEntrance = models.CharField(max_length=10 ,choices=APARTMENT_ENTRANCE_CHOICES, blank=True, null=True)
    parking = models.CharField(max_length=30, choices=[('ground', 'Наземная'), ('multiLevel', 'Многоуровневая'), ('underground', 'Подземная'), ('rooftop', 'На крыше')], blank=True, null=True)

    furniture = MultiSelectField(choices=FURNITURE_CHOICES, blank=True, null=True)
    bathroom = MultiSelectField(choices=BATHROOM_CHOICES, blank=True, null=True)
    apartment = MultiSelectField(choices=TECH_CHOICES, blank=True, null=True)
    connection = MultiSelectField(choices=COMMUNICATION_CHOICES, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    rent_per_month = models.PositiveIntegerField()
    currency_per_month = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')
    utilityPayment = models.CharField(max_length=70, choices=[('owner', 'Собственник'), ('tenant', 'Арендатор')])
    prepaymentPeriod = models.CharField(max_length=70, choices=PREPAYMENT_CHOICES, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')  # валюта аренды
    deposit = models.PositiveIntegerField(blank=True, null=True)
    rentalTerm = models.CharField(max_length=70, choices=[('several_months', 'Несколько месяцев'), ('year', 'От года')],null=True)
    livingConditions = models.CharField(max_length=100,choices=LIVING_CONDITIONS_CHOICES, blank=True, null=True, verbose_name='Условия проживания')
    phone = models.CharField(max_length=30)
    whatsApp = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        verbose_name = 'Аренда длительная продажа'
        verbose_name_plural = 'Аренда длительная продажа'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        # Валидация выбора мебели
        if 'no_furniture' in self.furniture and (len(self.furniture) > 1):
            raise ValidationError("Вы не можете выбрать 'Без мебели' с другими вариантами.")

class RentDayAdvertisement(models.Model):
    BATHROOM_CHOICES = [
        ('bath', 'Ванна'),
        ('showerRoom', 'Душевая кабина')
    ]

    TECH_CHOICES = [
        ('conditioner', 'Кондиционер'),
        ('fridge', 'Холодильник'),
        ('tv', 'Телевизор'),
        ('dishwasher', 'Посудомоечная машина'),
        ('washingmMachine', 'Стиральная машина')
    ]

    COMMUNICATION_CHOICES = [
        ('internet', 'Интернет'),
        ('phone', 'Телефон')
    ]
    FURNITURE_CHOICES = [
        ('noFurniture', 'Без мебели'),
        ('inKitchen', 'На кухне'),
        ('inRooms', 'В комнатах')
    ]
    PREPAYMENT_CHOICES = [
        ('1_month', 'За 1 месяц'),
        ('2_months', '2 месяца'),
        ('3_months', '3 месяца'),
        ('4+_months', '4+')
    ]
    CURRENCY_CHOICES = [
        ('MZN', 'MZN'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]
    LIVING_CONDITIONS_CHOICES = [
        ('allowed_with_children', 'Можно с детьми'),
        ('allowed_with_pets', 'Можно с животными')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  blank=True)
    accountType = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                   default='owner', blank=True)
    dealType = models.CharField(max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')], default='sale',
                                blank=True)
    estateType = models.CharField(max_length=50, choices=[('residential', 'Жилая')],
                                  blank=True, default='residential')
    leaseType = models.CharField(max_length=70, choices=[('longTerm', 'Длительно'), ('daily', 'Посуточно')], blank=True)
    obj = models.CharField(max_length=100, choices=[('flat', 'Квартира'), ('room', 'Комната'), ('house', 'Дом'), ('place', 'Койко-место')], blank=True)
    region = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=400, blank=True,null=True)
    nearest_stop = models.CharField(max_length=400, blank=True,null=True)
    minute_stop = models.CharField(max_length=400, blank=True,null=True)
    transport = models.CharField(max_length=20, choices=[('foot', 'Пешком'), ('car', 'Транспорт')], default='foot', blank=True)
    roomsNumber = models.CharField(max_length=20, choices=[
        ('Atelier', 'Студия'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6+', '6'),
        ('free_layout', 'Свободная планировка')
    ], blank=True)
    region = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=400, null=True)
    nearestStop = models.CharField(max_length=400, null=True)
    minutesBusStop = models.PositiveIntegerField(blank=True, null=True, default=0)
    pathType = models.CharField(max_length=20, choices=[('foot', 'Пешком'), ('transport', 'Транспорт')],
                                default='foot')
    floor = models.PositiveIntegerField()
    floorsHouse = models.PositiveIntegerField()
    flatNumber = models.PositiveIntegerField(blank=True, default=0)
    roomsNumber = models.CharField(max_length=20, choices=[
        ('studio', 'Студия'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('overSix', '6'),
        ('freePlanning', 'Свободная планировка')
    ])

    totalArea = models.PositiveIntegerField(blank=True, default=0)
    livingArea = models.PositiveIntegerField(blank=True, null=True)
    kitchenArea = models.PositiveIntegerField(blank=True, null=True)
    propertyType = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartments', 'Апартаменты')])
    photos = GenericRelation(AdvertisementPhoto)
    youtubeLink = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    daily_price = models.PositiveIntegerField(verbose_name='Цена за сутки', blank=True, default=0)
    daily_price_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN', blank=True)

    deposit = models.PositiveIntegerField(verbose_name='Залог', blank=True, default=0)
    deposit_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN', blank=True)



    furniture = MultiSelectField(choices=FURNITURE_CHOICES, blank=True, null=True)
    bathroom_choice = MultiSelectField(choices=BATHROOM_CHOICES, blank=True, null=True)
    tech = MultiSelectField(choices=TECH_CHOICES, blank=True, null=True)
    communication = MultiSelectField(choices=COMMUNICATION_CHOICES, blank=True, null=True)
    living_conditions = MultiSelectField(choices=LIVING_CONDITIONS_CHOICES, blank=True, null=True, verbose_name='Условия проживания')
    phone = models.CharField(max_length=30, blank=True)
    additional_phone = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        verbose_name = 'Аренда посуточная продажи'
        verbose_name_plural = 'Аренда посуточная продажа'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        # Валидация выбора мебели
        if 'no_furniture' in self.furniture and (len(self.furniture) > 1):
            raise ValidationError("Вы не можете выбрать 'Без мебели' с другими вариантами.")

class SaleCommercialAdvertisement(models.Model):
    CURRENCY_CHOICES = [
        ('MZN', 'MZN'),
        ('USD', 'Доллар'),
        ('EUR', 'Евро'),
    ]
    INFRASTRUCTURE_CHOICES = [
        ('carWash', 'Автомойка'),
        ('autoService', 'Автосервис'),
        ('pharmacy', 'Аптека'),
        ('clothingTailor', 'Ателье одежды'),
        ('atm', 'Банкомат'),
        ('swimmingPool', 'Бассейн'),
        ('buffet', 'Буфет'),
        ('exhibitionWarehouseComplex', 'Выставочно-складской комплекс'),
        ('hotel', 'Гостиница'),
        ('cafe', 'Кафе'),
        ('cinema', 'Кинотеатр'),
        ('conferenceHall', 'Конференц-зал'),
        ('medicalCenter', 'Медицинский центр'),
        ('miniMarket', 'Минимаркет'),
        ('notaryOffice', 'Нотариальная контора'),
        ('bankBranch', 'Отделение банка'),
        ('park', 'Парк'),
        ('restaurant', 'Ресторан'),
        ('beautySalon', 'Салон красоты'),
        ('warehouse', 'Складское помещение'),
        ('diningRoom', 'Столовая'),
        ('supermarket', 'Супермаркет'),
        ('shoppingArea', 'Торговая зона'),
        ('fitnessCenter', 'Фитнес-центр'),
        ('centralReception', 'Центральная рецепция'),
    ]
    TAX_CHOICES = [
        ('VAT_included', 'Ндс включен'),
        ('tax_exempt', 'Ндс не облагается'),
        ('simplified_tax', 'Упрощенная налогообложения'),
    ]

    AGENT_BONUS_CHOICES = [
        ('none', 'Нет'),
        ('fixed_sum', 'Фиксированная сумма'),
        ('percentage_of_deal', 'Процент от сделки'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                   default='owner', blank=True)
    dealType = models.CharField(max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')], default='sale',
                                blank=True)
    estateType = models.CharField(max_length=50, choices=[('residential', 'Жилая'), ('commercial', 'Коммерческая')],
                                  blank=True)

    obj = models.CharField(max_length=100, choices=[
        ('office', 'Офис'),
        ('building', 'Здание'),
        ('retail_space', 'Торговая площадь'),
        ('free_place', 'Помещение свободного назначения'),
        ('production', 'Производство'),
        ('warehouse', 'Склад'),
        ('garage', 'Гараж'),
        ('business', 'Бизнес'),
        ('commercial_land', 'Коммерческая земля')
    ])
    region = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=400, null=True)
    nearestStop = models.CharField(max_length=400, null=True)
    minutesBusStop = models.PositiveIntegerField(blank=True, null=True, default=0)
    pathType = models.CharField(max_length=20, choices=[('foot', 'Пешком'), ('transport', 'Транспорт')],
                                default='foot')
    taxNumber = models.PositiveIntegerField()
    totalArea = models.PositiveIntegerField()
    ceilingHeights = models.PositiveIntegerField(blank=True, null=True)
    floor = models.PositiveIntegerField()
    floorsHouse = models.PositiveIntegerField()
    legalAddress = models.BooleanField(blank=True,null=True)
    isRoomOccupied = models.BooleanField(blank=True, null=True)
    planning = models.CharField(max_length=30, choices=[('open', 'Открытая'), ('corridor', 'Коридор'), ('cabinet', 'Кабинетная')])
    numberWetSpots = models.CharField(max_length=50, blank=True, null=True, choices=[('false', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('more_five', '5 и больше')])
    electricPower = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=[('office_decoration', 'Офисная отделка'), ('finished', 'Под чистовую отделку'), ('major_repairs_required', 'Требуется капитальный ремонт'), ('cosmetic_repairs_required', 'Требуется косметический ремонт')])
    furniture_c = models.BooleanField(blank=True, null=True)
    access = models.CharField(max_length=30, blank=True, null=True, choices=[('free', 'Свободный'), ('passing_system', 'Пропускная система')])
    parking = models.CharField(max_length=30, blank=True, null=True, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')])
    numberParkingPlaces = models.PositiveIntegerField(blank=True, null=True)
    parkingFees = models.CharField(max_length=30, blank=True, null=True, choices=[('paid', 'Платная'), ('free', 'Бесплатная')])
    parkingPrice = models.PositiveIntegerField(blank=True, null=True)
    parkingCurreny = models.CharField(max_length=3,choices=CURRENCY_CHOICES, default='MZN')

    buildingName = models.CharField(max_length=200, blank=True, null=True)
    yearBuilt = models.PositiveIntegerField(blank=True, null=True)
    BUILDING_TYPE_CHOICES = [
        ('administrative_building', 'Административное здание'),
        ('business_center', 'Бизнес-центр'),
        ('shopping_center', 'Торговый центр'),
        ('warehouse_complex', 'Складской комплекс'),
        ('industrial_park', 'Промышленный парк'),
        ('production_complex', 'Производственный комплекс'),
        ('multifunctional_complex', 'Многофункциональный комплекс'),
        ('logistics_complex', 'Логистический комплекс'),
        ('outlet', 'Аутлет'),
        ('other', 'Другое'),
    ]
    buildingType = models.CharField(
        max_length=50,
        choices=BUILDING_TYPE_CHOICES,
        default='other',  # Optional: set a default value if needed
        blank=True
    )
    buildingClass = models.CharField(max_length=3, blank=True, null=True, choices=[('A', 'A'), ('A+', 'A+'), ('B', 'B'), ('B+', 'B+'), ('B-', 'B-'), ('C', 'C')])
    buildingArea = models.PositiveIntegerField(blank=True, null=True)
    PLOT_CHOICES = [
        ('owned', 'Owned'),
        ('leased', 'Leased'),
    ]

    plot = models.CharField(
        max_length=20,  # Adjust as needed
        blank=True,
        null=True
    )
    category = models.CharField(max_length=30, choices=[('valid', 'Действующее'), ('project', 'Проект'), ('under_construction', 'Строящееся')], blank=True)
    developer = models.CharField(max_length=200, blank=True, null=True)
    managementCompany = models.CharField(max_length=200, blank=True, null=True)
    ventilation = models.CharField(max_length=30, blank=True, null=True, choices=[('natural', 'Естественная'), ('inflow', 'Приточная'), ('none', 'Нет')])
    сonditioning = models.CharField(max_length=30, blank=True, null=True, choices=[('local', 'Местное'), ('center', 'Центральное'), ('none', 'Нет')])
    heating = models.CharField(max_length=30, blank=True, null=True, choices=[('autonomous', 'Автономное'), ('center', 'Центральное'), ('none', 'Нет')])
    fireExtinguishingSystem = models.CharField(max_length=30, blank=True, null=True, choices=[('hydrant', 'Гидрантная'), ('sprinkler', 'Спринклерная'), ('powder', 'Порошковая'), ('gas', 'Газовая'), ('alarm', 'Сигнализация'), ('false', 'Нет')])
    infrastructure = MultiSelectField(choices=INFRASTRUCTURE_CHOICES, blank=True, null=True)
    photos = GenericRelation(AdvertisementPhoto)
    youtubeLink = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    # Пример полей для цены
    total_price = models.PositiveIntegerField(verbose_name='Цена за всё', blank=True, null=True)
    price_per_m2 = models.PositiveIntegerField(verbose_name='Цена за м2', blank=True, null=True)
    currency_total = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')
    currency_per = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')
    # Поле для налога
    tax = models.CharField(max_length=50, choices=TAX_CHOICES, blank=True, null=True)

    # Поле для бонуса агенту
    agentBonus = models.CharField(max_length=50, choices=AGENT_BONUS_CHOICES, blank=True, null=True)

    # Поля для контактов
    phone = models.CharField(max_length=30, verbose_name='Телефон', blank=True, null=True)
    additional_phone = models.CharField(max_length=30, verbose_name='Дополнительный номер', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        verbose_name = 'Комерческие продажи'
        verbose_name_plural = 'Комерческая продажа'
    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        # Validate the 'plot' field to ensure it meets the requirements
        if self.plot is not None:
            if self.plot.isdigit():
                # It's a number; valid
                return
            elif self.plot in dict(self.PLOT_CHOICES):
                # It's a valid choice
                return
            else:
                raise ValidationError({
                    'plot': 'Must be a number or one of the following choices: "owned", "leased".'
                })

class RentCommercialAdvertisement(models.Model):


    CURRENCY_CHOICES = [
        ('MZN', 'MZN'),
        ('USD', 'Доллар'),
        ('EUR', 'Евро'),
    ]
    INFRASTRUCTURE_CHOICES = [
        ('carWash', 'Автомойка'),
        ('autoService', 'Автосервис'),
        ('pharmacy', 'Аптека'),
        ('clothingTailor', 'Ателье одежды'),
        ('atm', 'Банкомат'),
        ('swimmingPool', 'Бассейн'),
        ('buffet', 'Буфет'),
        ('exhibitionWarehouseComplex', 'Выставочно-складской комплекс'),
        ('hotel', 'Гостиница'),
        ('cafe', 'Кафе'),
        ('cinema', 'Кинотеатр'),
        ('conferenceHall', 'Конференц-зал'),
        ('medicalCenter', 'Медицинский центр'),
        ('miniMarket', 'Минимаркет'),
        ('notaryOffice', 'Нотариальная контора'),
        ('bankBranch', 'Отделение банка'),
        ('park', 'Парк'),
        ('restaurant', 'Ресторан'),
        ('beautySalon', 'Салон красоты'),
        ('warehouse', 'Складское помещение'),
        ('diningRoom', 'Столовая'),
        ('supermarket', 'Супермаркет'),
        ('shoppingArea', 'Торговая зона'),
        ('fitnessCenter', 'Фитнес-центр'),
        ('centralReception', 'Центральная рецепция'),
    ]
    TAX_CHOICES = [
        ('VAT_included', 'Ндс включен'),
        ('tax_exempt', 'Ндс не облагается'),
        ('simplified_tax', 'Упрощенная налогообложения'),
    ]

    AGENT_BONUS_CHOICES = [
        ('none', 'Нет'),
        ('fixed_sum', 'Фиксированная сумма'),
        ('percentage_of_deal', 'Процент от сделки'),
    ]


    COMMUNAL_PAYMENTS_CHOICES = [
        ('included', 'Включены'),
        ('not_included', 'Не включены'),
    ]

    OPERATING_COSTS_CHOICES = [
        ('included', 'Включены'),
        ('not_provided', 'Не предусмотрены'),
    ]

    RENT_TYPE_CHOICES = [
        ('long-term', 'Долгосрочная'),
        ('short-term', 'Краткосрочная'),
    ]
    PREPAYMENT_CHOICES = [
        ('4months', '4 мес'),
        ('5months', '5 мес'),
        ('6months', '6 мес'),
        ('7months', '7 мес'),
        ('8months', '8 мес'),
        ('9months', '9 мес'),
        ('10months', '10 мес'),
        ('11months', '11 мес'),
        ('1year', 'Год'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                   default='owner', blank=True)
    dealType = models.CharField(max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')], default='sale',
                                blank=True)
    estateType = models.CharField(max_length=50, choices=[('residential', 'Жилая'), ('commercial', 'Коммерческая')],
                                  blank=True)

    obj = models.CharField(max_length=100, choices=[
        ('office', 'Офис'),
        ('building', 'Здание'),
        ('retail_space', 'Торговая площадь'),
        ('free_place', 'Помещение свободного назначения'),
        ('production', 'Производство'),
        ('warehouse', 'Склад'),
        ('garage', 'Гараж'),
        ('business', 'Бизнес'),
        ('commercial_land', 'Коммерческая земля')
    ])

    region = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=400, null=True)
    nearestStop = models.CharField(max_length=400, null=True)
    minutesBusStop = models.PositiveIntegerField(blank=True, null=True, default=0)
    pathType = models.CharField(max_length=20, choices=[('foot', 'Пешком'), ('transport', 'Транспорт')],
                                default='foot')
    taxNumber = models.PositiveIntegerField()
    totalArea = models.PositiveIntegerField()
    ceilingHeights = models.PositiveIntegerField(blank=True, null=True)
    floor = models.PositiveIntegerField()
    floorsHouse = models.PositiveIntegerField()
    legalAddress = models.BooleanField(blank=True, null=True)
    isRoomOccupied = models.BooleanField(blank=True, null=True)
    planning = models.CharField(max_length=30,
                                choices=[('open', 'Открытая'), ('corridor', 'Коридор'), ('cabinet', 'Кабинетная')])
    numberWetSpots = models.CharField(max_length=50, blank=True, null=True,
                                      choices=[('false', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                               ('more_five', '5 и больше')])
    electricPower = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True,
                              choices=[('office_decoration', 'Офисная отделка'), ('finished', 'Под чистовую отделку'),
                                       ('major_repairs_required', 'Требуется капитальный ремонт'),
                                       ('cosmetic_repairs_required', 'Требуется косметический ремонт')])
    furniture_c = models.BooleanField(blank=True, null=True)
    access = models.CharField(max_length=30, blank=True, null=True,
                              choices=[('free', 'Свободный'), ('passing_system', 'Пропускная система')])
    parking = models.CharField(max_length=30, blank=True, null=True,
                               choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'),
                                        ('underground', 'Подземная'), ('in_roof', 'На крыше')])
    numberParkingPlaces = models.PositiveIntegerField(blank=True, null=True)
    parkingFees = models.CharField(max_length=30, blank=True, null=True,
                                   choices=[('paid', 'Платная'), ('free', 'Бесплатная')])
    parkingPrice = models.PositiveIntegerField(blank=True, null=True)
    parkingCurreny = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')

    buildingName = models.CharField(max_length=200)
    yearBuilt = models.PositiveIntegerField(blank=True, null=True)
    BUILDING_TYPE_CHOICES = [
        ('administrative_building', 'Административное здание'),
        ('business_center', 'Бизнес-центр'),
        ('shopping_center', 'Торговый центр'),
        ('warehouse_complex', 'Складской комплекс'),
        ('industrial_park', 'Промышленный парк'),
        ('production_complex', 'Производственный комплекс'),
        ('multifunctional_complex', 'Многофункциональный комплекс'),
        ('logistics_complex', 'Логистический комплекс'),
        ('outlet', 'Аутлет'),
        ('other', 'Другое'),
    ]
    buildingType = models.CharField(
        max_length=50,
        choices=BUILDING_TYPE_CHOICES,
        default='other',  # Optional: set a default value if needed
        blank=True
    )
    buildingClass = models.CharField(max_length=3, blank=True, null=True,
                                     choices=[('A', 'A'), ('A+', 'A+'), ('B', 'B'), ('B+', 'B+'), ('B-', 'B-'),
                                              ('C', 'C')])
    buildingArea = models.PositiveIntegerField(blank=True, null=True)
    PLOT_CHOICES = [
        ('owned', 'Owned'),
        ('leased', 'Leased'),
    ]

    plot = models.CharField(
        max_length=20,  # Adjust as needed
        blank=True,
        null=True
    )
    category = models.CharField(max_length=30, choices=[('valid', 'Действующее'), ('project', 'Проект'),
                                                        ('under_construction', 'Строящееся')], blank=True)
    developer = models.CharField(max_length=200, blank=True, null=True)
    managementCompany = models.CharField(max_length=200, blank=True, null=True)
    ventilation = models.CharField(max_length=30, blank=True, null=True,
                                   choices=[('natural', 'Естественная'), ('inflow', 'Приточная'), ('none', 'Нет')])
    сonditioning = models.CharField(max_length=30, blank=True, null=True,
                                    choices=[('local', 'Местное'), ('center', 'Центральное'), ('none', 'Нет')])
    heating = models.CharField(max_length=30, blank=True, null=True,
                               choices=[('autonomous', 'Автономное'), ('center', 'Центральное'), ('none', 'Нет')])
    fireExtinguishingSystem = models.CharField(max_length=30, blank=True, null=True,
                                               choices=[('hydrant', 'Гидрантная'), ('sprinkler', 'Спринклерная'),
                                                        ('powder', 'Порошковая'), ('gas', 'Газовая'),
                                                        ('alarm', 'Сигнализация'), ('false', 'Нет')])
    infrastructure = MultiSelectField(choices=INFRASTRUCTURE_CHOICES, blank=True, null=True)
    photos = GenericRelation(AdvertisementPhoto)
    youtubeLink = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)


    rent_per_month_per_m2 = models.PositiveIntegerField(verbose_name='Аренда в месяц за м2', blank=True, null=True)
    rent_per_year_per_m2 = models.PositiveIntegerField(verbose_name='Аренда в год за м2', blank=True, null=True)
    rent_per_month = models.PositiveIntegerField(verbose_name='Аренда в месяц', blank=True, null=True)
    currency_rent_month_per_m2 = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')
    currency_rent_year_per_m2 = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')
    currency_rent_month = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')

    # Поле для налога
    tax = models.CharField(max_length=50, choices=TAX_CHOICES, blank=True, null=True)

    # Поле для коммунальных платежей
    utilityPayment = models.BooleanField(blank=True,null=True)

    # Поле для эксплуатационных расходов
    operatingCosts = models.BooleanField(blank=True, null=True)

    # Поле для типа аренды
    rentalType = models.CharField(max_length=50, choices=RENT_TYPE_CHOICES, blank=True, null=True)

    # Поле для минимального срока аренды
    minimumLeaseTerm = models.PositiveIntegerField(verbose_name='Минимальный срок аренды (в месяцах)', blank=True,
                                                  null=True)

    rentalHolidays = models.BooleanField(blank=True,null=True)
    # Поле для обеспечительного платежа
    security_deposit = models.PositiveIntegerField(verbose_name='Обеспечительный платеж', blank=True, null=True)
    currency_deposit = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MZN')

    # Поле для предоплаты
    prepayment = models.CharField(max_length=15, choices=PREPAYMENT_CHOICES, default='year')

    # Поле для бонуса агенту
    agentBonus = models.CharField(max_length=50, choices=AGENT_BONUS_CHOICES, default='false')

    # Поля для контактов
    phone = models.CharField(max_length=30, verbose_name='Телефон', blank=True, null=True)
    additional_phone = models.CharField(max_length=30, verbose_name='Дополнительный номер', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        verbose_name = 'Комерческие аренды'
        verbose_name_plural = 'Комерческая аренда'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        # Validate the 'plot' field to ensure it meets the requirements
        if self.plot is not None:
            if self.plot.isdigit():
                # It's a number; valid
                return
            elif self.plot in dict(self.PLOT_CHOICES):
                # It's a valid choice
                return
            else:
                raise ValidationError({
                    'plot': 'Must be a number or one of the following choices: "owned", "leased".'
                })