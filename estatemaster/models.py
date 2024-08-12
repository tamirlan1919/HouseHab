from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from .managers import CustomUserManager



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

class RentalSpecialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Аренда недвижимости'
        verbose_name_plural = 'Аренда недвижимости'


class MortgageSpecialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Ипотечное кредитование'
        verbose_name_plural = 'Ипотечное кредитование'
class OtherServiceSpecialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Другие услуги'
        verbose_name_plural = 'Другие услуги'

class SaleSpecialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продажа недвижимости'
        verbose_name_plural = 'Продажа недвижимости'


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
        ('into_the_courtyard', 'Во двор'),
        ('to_sea', 'На море')
    ]
    APARTMENT_ENTRANCE_CHOICES = [
        ('ramp', 'Пандус'),
        ('garbage_chute', 'Мусоропровод')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner',blank=True)
    dealType = models.CharField(max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')],default='sale',blank=True)
    estateType = models.CharField(max_length=50, choices=[('residential', 'Жилая'), ('commercial','Коммерческая')],blank=True)
    obj = models.CharField(max_length=100, choices=[
        ('flat', 'Квартира'),
        ('new_flat', 'Квартира в новостройке'),
        ('room', 'Комната'),
        ('part_flat', 'Доля в квартире'),
        ('house', 'Дом'),
        ('cottage', 'Коттедж'),
        ('townhouse', 'Таунхаус'),
        ('part_house', 'Часть дома'),
        ('spot', 'Участок')
    ])
    new_or_no = models.CharField(max_length=20, choices=[('second', 'Вторичка'), ('new', 'Новостройка')], default='second', blank=True, null=True)
    region = models.OneToOneField(Location, on_delete=models.CASCADE,blank=True, null=True)
    address = models.CharField(max_length=400)
    nearest_stop = models.CharField(max_length=400)
    minute_stop = models.CharField(max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot')
    floor = models.PositiveIntegerField()
    floors_house = models.PositiveIntegerField()
    number_flat = models.CharField(max_length=30, blank=True, null=True)
    age_build = models.PositiveIntegerField(blank=True, null=True)
    ceiling_height = models.FloatField(blank=True, null=True)
    houseType = models.CharField(max_length=100, choices=[
        ('brick', 'Кирпичный'),
        ('monolit', 'Монолитный'),
        ('panel', 'Панельный'),
        ('block', 'Блочный'),
        ('wood', 'Деревянный'),
    ])
    roomsNumber = models.CharField(max_length=20, choices=[
        ('Atelier', 'Студия'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6+', '6'),
        ('free_layout', 'Свободная планировка')
    ])
    total_area = models.PositiveIntegerField()
    living_area = models.PositiveIntegerField(blank=True, null=True)
    kitchen_area = models.PositiveIntegerField(blank=True, null=True)
    propertyType = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')],blank=True)
    photo = models.ImageField(upload_to='images/',blank=True)
    video = models.CharField(max_length=300, blank=True, null=True)

    balconies = models.PositiveIntegerField(default=0)
    loggia = models.PositiveIntegerField(default=0)

    bathroom = models.PositiveIntegerField(default=0)
    bathroom_joint = models.PositiveIntegerField(default=0)
    repair = models.CharField(max_length=70, choices=[('without_repair', 'Без ремонта'), ('cosmetic', 'Косметический'), ('euro', 'Евро'), ('designer', 'Дизайнерский')], blank=True, null=True)
    elevators_passengers = models.PositiveIntegerField(default=0)
    elevators_cargo = models.PositiveIntegerField(default=0)
    viewFromWindow = MultiSelectField(choices=VIEW_CHOICES, blank=True, null=True)
    apartmentEntrance = MultiSelectField(choices=APARTMENT_ENTRANCE_CHOICES, blank=True, null=True)
    parking = models.CharField(max_length=30, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')], blank=True, null=True)
    headings = models.CharField(max_length=100)
    description = models.TextField()
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    saleType = models.CharField(max_length=50, choices=[('only_sale', 'Только продаю'), ('sale_another', 'Одновременно покупаю другую')],blank=True)
    phone = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=300)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Жилые прожажи'
        verbose_name_plural = 'Жилая продажа'

    def __str__(self):
        return self.headings



class RentLongAdvertisement(models.Model):
    VIEW_CHOICES = [
        ('outside', 'На улицу'),
        ('into_the_courtyard', 'Во двор'),
        ('to_sea', 'На море')
    ]
    APARTMENT_ENTRANCE_CHOICES = [
        ('ramp', 'Пандус'),
        ('garbage_chute', 'Мусоропровод')
    ]
    BATHROOM_CHOICES = [
        ('bath', 'Ванна'),
        ('shower', 'Душевая кабина')
    ]

    TECH_CHOICES = [
        ('ac', 'Кондиционер'),
        ('fridge', 'Холодильник'),
        ('tv', 'Телевизор'),
        ('dishwasher', 'Посудомоечная машина'),
        ('washing_machine', 'Стиральная машина')
    ]

    COMMUNICATION_CHOICES = [
        ('internet', 'Интернет'),
        ('phone', 'Телефон')
    ]
    FURNITURE_CHOICES = [
        ('no_furniture', 'Без мебели'),
        ('kitchen', 'На кухне'),
        ('rooms', 'В комнатах')
    ]
    PREPAYMENT_CHOICES = [
        ('1_month', 'За 1 месяц'),
        ('2_months', '2 месяца'),
        ('3_months', '3 месяца'),
        ('4_plus', '4+')
    ]
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    LIVING_CONDITIONS_CHOICES = [
        ('children_allowed', 'Можно с детьми'),
        ('pets_allowed', 'Можно с животными')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                   default='owner', blank=True)
    dealType = models.CharField(max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')], default='sale',
                                blank=True)
    estateType = models.CharField(max_length=50, choices=[('residential', 'Жилая'), ('commercial', 'Коммерческая')],
                                  blank=True)
    type_rent_long = models.CharField(max_length=70, choices=[('long', 'Длительно'), ('day', 'Посуточно')])

    obj = models.CharField(max_length=100, choices=[
        ('flat', 'Квартира'),
        ('new_flat', 'Квартира в новостройке'),
        ('room', 'Комната'),
        ('part_flat', 'Доля в квартире'),
        ('house', 'Дом'),
        ('cottage', 'Коттедж'),
        ('townhouse', 'Таунхаус'),
        ('part_house', 'Часть дома'),
        ('spot', 'Участок')
    ])
    new_or_no = models.CharField(max_length=20, choices=[('second', 'Вторичка'), ('new', 'Новостройка')], default='second', blank=True, null=True)
    region = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=400)
    nearest_stop = models.CharField(max_length=400)
    minute_stop = models.CharField(max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot')
    roomsNumber = models.CharField(max_length=20, choices=[
        ('Atelier', 'Студия'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6+', '6'),
        ('free_layout', 'Свободная планировка')
    ])
    floor = models.PositiveIntegerField()
    floors_house = models.PositiveIntegerField()
    number_flat = models.CharField(max_length=30, blank=True, null=True)
    total_area = models.PositiveIntegerField()
    living_area = models.PositiveIntegerField(blank=True, null=True)
    kitchen_area = models.PositiveIntegerField(blank=True, null=True)
    propertyType = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')])
    photo = models.ImageField(upload_to='images/', blank=True)
    video = models.CharField(max_length=300, blank=True, null=True)

    viewFromWindow = MultiSelectField(choices=VIEW_CHOICES, blank=True, null=True)
    balconies = models.PositiveIntegerField(default=0)
    loggia = models.PositiveIntegerField(default=0)
    bathroom_count = models.PositiveIntegerField(default=0, verbose_name='Количество ванных комнат')
    bathroom_joint_count = models.PositiveIntegerField(default=0, verbose_name='Количество совмещенных ванных комнат')
    repair = models.CharField(max_length=70, choices=[('without_repair', 'Без ремонта'), ('cosmetic', 'Косметический'), ('euro', 'Евро'), ('designer', 'Дизайнерский')], blank=True, null=True)
    elevators_passengers = models.PositiveIntegerField(default=0)
    elevators_cargo = models.PositiveIntegerField(default=0)
    apartmentEntrance = MultiSelectField(choices=APARTMENT_ENTRANCE_CHOICES, blank=True, null=True)
    parking = models.CharField(max_length=30, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')], blank=True, null=True)
    rent_per_month = models.PositiveIntegerField()
    utility_payer = models.CharField(max_length=70, choices=[('owner', 'Собственник'), ('tenant', 'Арендатор')])
    prepayment = models.CharField(max_length=70, choices=PREPAYMENT_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')  # валюта аренды
    deposit = models.PositiveIntegerField(blank=True, null=True)
    rental_period = models.CharField(max_length=70, choices=[('few_months', 'Несколько месяцев'), ('from_the_year', 'От года')])
    living_conditions = MultiSelectField(choices=LIVING_CONDITIONS_CHOICES, blank=True, null=True, verbose_name='Условия проживания')
    phone = models.CharField(max_length=30)
    additional_phone = models.CharField(max_length=30, blank=True, null=True)
    communication_method = models.CharField(max_length=70, choices=[('calls_and_messages', 'Звонки и сообщения'), ('whatsapp', 'WhatsApp'), ('only_calls', 'Только звонки')])
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    furniture = MultiSelectField(choices=FURNITURE_CHOICES, blank=True, null=True)
    bathroom_choice = MultiSelectField(choices=BATHROOM_CHOICES, blank=True, null=True)
    tech = MultiSelectField(choices=TECH_CHOICES, blank=True, null=True)
    communication = MultiSelectField(choices=COMMUNICATION_CHOICES, blank=True, null=True)
    headings = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = 'Аренда длительная продажа'
        verbose_name_plural = 'Аренда длительная продажа'

    def __str__(self):
        return self.headings

    def clean(self):
        super().clean()
        # Валидация выбора мебели
        if 'no_furniture' in self.furniture and (len(self.furniture) > 1):
            raise ValidationError("Вы не можете выбрать 'Без мебели' с другими вариантами.")

class RentDayAdvertisement(models.Model):
    VIEW_CHOICES = [
        ('outside', 'На улицу'),
        ('into_the_courtyard', 'Во двор'),
        ('to_sea', 'На море')
    ]
    APARTMENT_ENTRANCE_CHOICES = [
        ('ramp', 'Пандус'),
        ('garbage_chute', 'Мусоропровод')
    ]
    BATHROOM_CHOICES = [
        ('bath', 'Ванна'),
        ('shower', 'Душевая кабина')
    ]

    TECH_CHOICES = [
        ('ac', 'Кондиционер'),
        ('fridge', 'Холодильник'),
        ('tv', 'Телевизор'),
        ('dishwasher', 'Посудомоечная машина'),
        ('washing_machine', 'Стиральная машина')
    ]

    COMMUNICATION_CHOICES = [
        ('internet', 'Интернет'),
        ('phone', 'Телефон')
    ]
    FURNITURE_CHOICES = [
        ('no_furniture', 'Без мебели'),
        ('kitchen', 'На кухне'),
        ('rooms', 'В комнатах')
    ]
    PREPAYMENT_CHOICES = [
        ('1_month', 'За 1 месяц'),
        ('2_months', '2 месяца'),
        ('3_months', '3 месяца'),
        ('4_plus', '4+')
    ]
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    LIVING_CONDITIONS_CHOICES = [
        ('children_allowed', 'Можно с детьми'),
        ('pets_allowed', 'Можно с животными')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  blank=True)
    accountType = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                   default='owner', blank=True)
    dealType = models.CharField(max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')], default='sale',
                                blank=True)
    estateType = models.CharField(max_length=50, choices=[('residential', 'Жилая')],
                                  blank=True, default='residential')
    type_rent_long = models.CharField(max_length=70, choices=[('long', 'Длительно'), ('day', 'Посуточно')], blank=True, default='day')

    obj = models.CharField(max_length=100, choices=[('flat', 'Квартира'), ('room', 'Комната'), ('house', 'Дом'), ('place', 'Койко-место')], blank=True)
    new_or_no = models.CharField(max_length=20, choices=[('second', 'Вторичка'), ('new', 'Новостройка')], default='second', blank=True, null=True)
    region = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=400, blank=True)
    nearest_stop = models.CharField(max_length=400, blank=True)
    minute_stop = models.CharField(max_length=400, blank=True)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot', blank=True)
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
    floor = models.PositiveIntegerField(blank=True, default=0)
    floors_house = models.PositiveIntegerField(blank=True, default=0)
    number_flat = models.CharField(max_length=30, blank=True)
    total_area = models.PositiveIntegerField(blank=True, default=0)
    kitchen_area = models.PositiveIntegerField(blank=True, default=0)
    propertyType = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')],blank=True)
    guest_count = models.PositiveIntegerField(blank=True, default=0)
    photo = models.ImageField(upload_to='images/', blank=True)
    video = models.CharField(max_length=300, blank=True, null=True)
    headings = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    daily_price = models.PositiveIntegerField(verbose_name='Цена за сутки', blank=True, default=0)
    daily_price_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn', blank=True)

    deposit = models.PositiveIntegerField(verbose_name='Залог', blank=True, default=0)
    deposit_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn', blank=True)

    furniture = MultiSelectField(choices=FURNITURE_CHOICES, blank=True, null=True)
    bathroom_choice = MultiSelectField(choices=BATHROOM_CHOICES, blank=True, null=True)
    tech = MultiSelectField(choices=TECH_CHOICES, blank=True, null=True)
    communication = MultiSelectField(choices=COMMUNICATION_CHOICES, blank=True, null=True)
    living_conditions = MultiSelectField(choices=LIVING_CONDITIONS_CHOICES, blank=True, null=True, verbose_name='Условия проживания')
    phone = models.CharField(max_length=30, blank=True)
    additional_phone = models.CharField(max_length=30, blank=True, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Аренда посуточная продажи'
        verbose_name_plural = 'Аренда посуточная продажа'

    def __str__(self):
        return self.headings

    def clean(self):
        super().clean()
        # Валидация выбора мебели
        if 'no_furniture' in self.furniture and (len(self.furniture) > 1):
            raise ValidationError("Вы не можете выбрать 'Без мебели' с другими вариантами.")

class SaleCommercialAdvertisement(models.Model):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner')
    region = models.OneToOneField(Location, on_delete=models.CASCADE, blank=True, null=True)
    deal_type = models.CharField(max_length=100, choices=[('sale', 'Продажа')])
    type_of_property = models.CharField(max_length=50, choices=[('commercial', 'Коммерческая')])
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
    address = models.CharField(max_length=400)
    nearest_stop = models.CharField(max_length=400)
    minute_stop = models.CharField(max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot')
    number_nalog = models.CharField(max_length=100)
    total_area = models.PositiveIntegerField()
    ceiling_height = models.PositiveIntegerField(blank=True, null=True)
    floor = models.PositiveIntegerField()
    floors_house = models.PositiveIntegerField()
    ur_address = models.CharField(max_length=200, choices=[('provided', 'Предоставляется'), ('not_provided', 'Не предоставляется')])
    room_busy = models.BooleanField(default=False)
    layout = models.CharField(max_length=30, choices=[('open', 'Открытая'), ('corridor', 'Коридор'), ('cabinet', 'Кабинетная')])
    count_rooms = models.CharField(max_length=50, blank=True, null=True, choices=[('no', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 и больше')])
    electric = models.PositiveIntegerField(blank=True, null=True)
    condition = models.CharField(max_length=100, blank=True, null=True, choices=[('office', 'Офисная отделка'), ('clean_ot', 'Под чистовую отделку'), ('cap_repair', 'Требуется капитальный ремонт'), ('cosmetic_repair', 'Требуется косметический ремонт')])
    mebel = models.BooleanField(default=False)
    access = models.CharField(max_length=30, blank=True, null=True, choices=[('free', 'Свободный'), ('propusk', 'Пропускная система')])
    parking = models.CharField(max_length=30, blank=True, null=True, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')])
    numner_seats = models.PositiveIntegerField(blank=True, null=True)
    price_park = models.CharField(max_length=30, blank=True, null=True, choices=[('paid', 'Платная'), ('free', 'Бесплатная')])
    price_month = models.PositiveIntegerField(blank=True, null=True)
    name_building = models.CharField(max_length=200)
    age_build = models.PositiveIntegerField(blank=True, null=True)
    type_building = models.CharField(max_length=100, blank=True, null=True)
    klass_zd = models.CharField(max_length=3, blank=True, null=True, choices=[('A', 'A'), ('A+', 'A+'), ('B', 'B'), ('B+', 'B+'), ('B-', 'B-'), ('C', 'C')])
    area_zd = models.PositiveIntegerField(blank=True, null=True)
    uchastok = models.PositiveIntegerField(blank=True, null=True)
    in_sobstven = models.BooleanField(default=False)
    in_rent = models.BooleanField(default=False)
    category = models.CharField(max_length=30, choices=[('doing', 'Действующее'), ('project', 'Проект'), ('building', 'Строящееся')])
    developer = models.CharField(max_length=200, blank=True, null=True)
    upr_company = models.CharField(max_length=200, blank=True, null=True)
    ventilation = models.CharField(max_length=30, blank=True, null=True, choices=[('natural', 'Естественная'), ('supply', 'Приточная'), ('no', 'Нет')])
    conditioning = models.CharField(max_length=30, blank=True, null=True, choices=[('local', 'Местное'), ('center', 'Центральное'), ('no', 'Нет')])
    heating = models.CharField(max_length=30, blank=True, null=True, choices=[('auto', 'Автономное'), ('center', 'Центральное'), ('no', 'Нет')])
    fire_stop = models.CharField(max_length=30, blank=True, null=True, choices=[('gidro', 'Гидрантная'), ('sprinkler', 'Спринклерная'), ('powder', 'Порошковая'), ('gas', 'Газовая'), ('signal', 'Сигнализация'), ('no', 'Нет')])
    auto_wish = models.BooleanField(default=False)
    auto_service = models.BooleanField(default=False)
    pharmacy = models.BooleanField(default=False)
    atelier = models.BooleanField(default=False)
    bank = models.BooleanField(default=False)
    bufet = models.BooleanField(default=False)
    sclad = models.BooleanField(default=False)
    hotel = models.BooleanField(default=False)
    cafe = models.BooleanField(default=False)
    tv_vinema = models.BooleanField(default=False)
    conference = models.BooleanField(default=False)
    med_center = models.BooleanField(default=False)
    mini_market = models.BooleanField(default=False)
    notarial_contore = models.BooleanField(default=False)
    otdel_bank = models.BooleanField(default=False)
    park = models.BooleanField(default=False)
    restoran = models.BooleanField(default=False)
    beaty_salon = models.BooleanField(default=False)
    sclad_place = models.BooleanField(default=False)
    stolov = models.BooleanField(default=False)
    supermarket = models.BooleanField(default=False)
    torg_zona = models.BooleanField(default=False)
    fitness = models.BooleanField(default=False)
    central_recep = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images/',blank=True)
    video = models.CharField(max_length=300, blank=True, null=True)
    headings = models.CharField(max_length=100)
    description = models.TextField()
    currency_all = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    price_all = models.PositiveIntegerField()
    currency_kv_m = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    price_kv_m = models.PositiveIntegerField()
    is_nalog = models.CharField(max_length=70, choices=[('nds_on', 'НДС включен'), ('nds_off', 'НДС не облагается')
        , ('just_nalog', 'Упрощенная налогобложение')])
    bonus_agent = models.CharField(max_length=70, choices=[('no', 'Нет'), ('fix_sum', 'Фиксированная сумма'),
                                                           ('procent', 'Процент от сделки')])
    phone = models.CharField(max_length=30)
    dop_phone = models.CharField(max_length=30)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        verbose_name = 'Комерческие продажи'
        verbose_name_plural = 'Комерческая продажа'
    def __str__(self):
        return self.headings

class RentCommercialAdvertisement(models.Model):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner')
    deal_type = models.CharField(max_length=100, choices=[('rent', 'Аренда')])
    region = models.OneToOneField(Location, on_delete=models.CASCADE,blank=True, null=True)

    type_of_property = models.CharField(max_length=50, choices=[('commercial', 'Коммерческая')])
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
    address = models.CharField(max_length=400)
    nearest_stop = models.CharField(max_length=400)
    minute_stop = models.CharField(max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot')
    number_nalog = models.CharField(max_length=100)
    total_area = models.PositiveIntegerField()
    ceiling_height = models.PositiveIntegerField(blank=True, null=True)
    floor = models.PositiveIntegerField()
    floors_house = models.PositiveIntegerField()
    ur_address = models.CharField(max_length=200, choices=[('provided', 'Предоставляется'), ('not_provided', 'Не предоставляется')])
    room_busy = models.BooleanField(default=False)
    layout = models.CharField(max_length=30, choices=[('open', 'Открытая'), ('corridor', 'Коридор'), ('cabinet', 'Кабинетная')])
    count_rooms = models.CharField(max_length=50, blank=True, null=True, choices=[('no', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 и больше')])
    electric = models.PositiveIntegerField(blank=True, null=True)
    condition = models.CharField(max_length=100, blank=True, null=True, choices=[('office', 'Офисная отделка'), ('clean_ot', 'Под чистовую отделку'), ('cap_repair', 'Требуется капитальный ремонт'), ('cosmetic_repair', 'Требуется косметический ремонт')])
    mebel = models.BooleanField(default=False)
    access = models.CharField(max_length=30, blank=True, null=True, choices=[('free', 'Свободный'), ('propusk', 'Пропускная система')])
    parking = models.CharField(max_length=30, blank=True, null=True, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')])
    numner_seats = models.PositiveIntegerField(blank=True, null=True)
    price_park = models.CharField(max_length=30, blank=True, null=True, choices=[('paid', 'Платная'), ('free', 'Бесплатная')])
    price_month = models.PositiveIntegerField(blank=True, null=True)
    name_building = models.CharField(max_length=200)
    age_build = models.PositiveIntegerField(blank=True, null=True)
    type_building = models.CharField(max_length=100, blank=True, null=True)
    klass_zd = models.CharField(max_length=3, blank=True, null=True, choices=[('A', 'A'), ('A+', 'A+'), ('B', 'B'), ('B+', 'B+'), ('B-', 'B-'), ('C', 'C')])
    area_zd = models.PositiveIntegerField(blank=True, null=True)
    uchastok = models.PositiveIntegerField(blank=True, null=True)
    in_sobstven = models.BooleanField(default=False)
    in_rent = models.BooleanField(default=False)
    category = models.CharField(max_length=30, choices=[('doing', 'Действующее'), ('project', 'Проект'), ('building', 'Строящееся')])
    developer = models.CharField(max_length=200, blank=True, null=True)
    upr_company = models.CharField(max_length=200, blank=True, null=True)
    ventilation = models.CharField(max_length=30, blank=True, null=True, choices=[('natural', 'Естественная'), ('supply', 'Приточная'), ('no', 'Нет')])
    conditioning = models.CharField(max_length=30, blank=True, null=True, choices=[('local', 'Местное'), ('center', 'Центральное'), ('no', 'Нет')])
    heating = models.CharField(max_length=30, blank=True, null=True, choices=[('auto', 'Автономное'), ('center', 'Центральное'), ('no', 'Нет')])
    fire_stop = models.CharField(max_length=30, blank=True, null=True, choices=[('gidro', 'Гидрантная'), ('sprinkler', 'Спринклерная'), ('powder', 'Порошковая'), ('gas', 'Газовая'), ('signal', 'Сигнализация'), ('no', 'Нет')])
    auto_wish = models.BooleanField(default=False)
    auto_service = models.BooleanField(default=False)
    pharmacy = models.BooleanField(default=False)
    atelier = models.BooleanField(default=False)
    bank = models.BooleanField(default=False)
    bufet = models.BooleanField(default=False)
    sclad = models.BooleanField(default=False)
    hotel = models.BooleanField(default=False)
    cafe = models.BooleanField(default=False)
    tv_vinema = models.BooleanField(default=False)
    conference = models.BooleanField(default=False)
    med_center = models.BooleanField(default=False)
    mini_market = models.BooleanField(default=False)
    notarial_contore = models.BooleanField(default=False)
    otdel_bank = models.BooleanField(default=False)
    park = models.BooleanField(default=False)
    restoran = models.BooleanField(default=False)
    beaty_salon = models.BooleanField(default=False)
    sclad_place = models.BooleanField(default=False)
    stolov = models.BooleanField(default=False)
    supermarket = models.BooleanField(default=False)
    torg_zona = models.BooleanField(default=False)
    fitness = models.BooleanField(default=False)
    central_recep = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images/',blank=True)
    video = models.CharField(max_length=300, blank=True, null=True)
    headings = models.CharField(max_length=100)
    description = models.TextField()
    currency_month_kv_m = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    rent_month_kv_m = models.PositiveIntegerField()
    currency_kv_m_year = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    price_kv_m_year = models.PositiveIntegerField()
    currency_rent_month = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    rent_month = models.PositiveIntegerField()
    is_nalog = models.CharField(max_length=70, choices=[('nds_on', 'НДС включен'), ('nds_off', 'НДС не облагается'), ('just_nalog', 'Упрощенная налогобложение')])
    is_communal = models.BooleanField(default=False)
    is_exploitation = models.BooleanField(default=False)
    type_rent = models.CharField(max_length=30, choices=[('direct_rental', 'Прямая аренда'), ('subrent', 'Субаренда')])
    min_rent_period = models.PositiveIntegerField()
    rent_holidays = models.BooleanField(default=False)
    security_deposit = models.PositiveIntegerField()
    security_deposit_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    prepayment = models.CharField(max_length=30, choices=[
        ('4', '4 мес'),
        ('5', '5 мес'),
        ('6', '6 мес'),
        ('7', '7 мес'),
        ('8', '8 мес'),
        ('9', '9 мес'),
        ('10', '10 мес'),
        ('11', '11 мес'),
        ('year', 'Год')
    ])
    bonus_agent = models.CharField(max_length=70, choices=[('no', 'Нет'), ('fix_sum', 'Фиксированная сумма'), ('procent', 'Процент от сделки')])
    phone = models.CharField(max_length=30)
    dop_phone = models.CharField(max_length=30)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Комерческие аренды'
        verbose_name_plural = 'Комерческая аренда'

    def __str__(self):
        return self.headings

