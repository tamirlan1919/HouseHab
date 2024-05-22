from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    account_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('professional', 'Professional')],
                                    default='individual')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'account_type']
    objects = CustomUserManager()  # Используем кастомный менеджер для этой модели пользователя




    # Добавляем related_name для связей с группами и правами доступа
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
    cost_per_day = models.FloatField()
    discount_7_days = models.FloatField(default=0.10)
    discount_14_days = models.FloatField(default=0.15)
    discount_30_days = models.FloatField(default=0.20)

    def __str__(self):
        return self.get_promotion_type_display()


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


class ResidentialSaleListing(models.Model):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                    default='owner')
    type_of_deal = models.CharField(name='Тип сделки' ,max_length=40, default='Продажа')
    type_of_property = models.CharField(name = 'Тип недвижимости',max_length=50, default='Жилая')
    obj = models.CharField(name = 'Объект', max_length=100,
                           choices=[('flat', 'Квартира'), ('new_flat', 'Квартира в новостройке'),
                                    ('room','Комната'), ('part_flat','Доля в квартире'), ('house', 'Дом'),
                                    ('cottege','Коттедж'), ('tanhouse', 'Танхаус'), ('part_house', 'Часть дома'), ('spot','Участок')],
                          default='owner' )
    address = models.CharField(name='Адресс',max_length=400)
    nearest_stop = models.CharField(name='Ближайшая остановка',max_length=400)
    minute_stop = models.CharField(name='Минут до остановки',max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')],
                                    default='afoot')
    floor = models.PositiveIntegerField()
    floors_house = models.PositiveIntegerField()
    number_flat = models.CharField(max_length=30,name='Номер квартиры')
    age_build = models.PositiveIntegerField()
    ceiling_height = models.PositiveIntegerField(name='Высота потолков')
    type_house = models.CharField(max_length=20, choices=[('brick', 'Кирпичный'), ('monolithic', 'Монолитный'),
                                                          ('panel', 'Панельный'), ('block', 'Блочный'), ('wooden', 'Деревянный')])
    count_rooms = models.CharField(max_length=20, choices=[('Atelier', 'Студия'), ('1', '1'),
                                                          ('2', '2'), ('3', '3'), ('4', '4'),
                                                           ('5', '5'), ('6+', '6'), ('free_layout', 'Свободная планировка')])
    total_area = models.PositiveIntegerField(name='Общая площадь')
    living_area = models.PositiveIntegerField(name='Жилая площадь')
    kitchen_area = models.PositiveIntegerField(name='Кухня')
    property_type = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')])
    photo = models.ImageField(upload_to='images/')
    video = models.CharField(max_length=300,name='Видео')
    balconies = models.PositiveIntegerField(name='Балконы',default=0)
    loggia = models.PositiveIntegerField(name='Лоджия',default=0)
    view_from_window = models.CharField(max_length=30, choices=[('outside', 'На улицу'), ('into_the_courtyard', 'Во двор')])
    bathroom = models.PositiveIntegerField(name='Раздельный',default=0)
    bathroom_joint = models.PositiveIntegerField(name='Совмещенный',default=0)
    repair = models.CharField(max_length=70, choices=[('without_repair', 'Без ремонта'), ('cosmetic', 'Космитический'),
                                                      ('euro',"Евро"),('disigner', 'Дизайнерский')])
    elevators_passengers = models.PositiveIntegerField(name='Пассажирский',default=0)
    elevators_cargo = models.PositiveIntegerField(name='Грузовой',default=0)
    entrance = models.CharField(max_length=30, choices=[('ramp', 'Пандус'), ('garbage_chute', 'Мусоропровод')])
    parking = models.CharField(max_length=30, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'),
                                                       ('underground','Подземная'), ('in_roof','На крыше')])
    headings = models.CharField(max_length=100,name='Загаловок')
    description = models.TextField(name='Описание')
    price = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='mzn')

    ipoteka = models.CharField(max_length=30, choices=[('perhaps', 'Возможно'), ('no', 'Нет')])
    how_sell = models.CharField(max_length=30, choices=[('only_sell', 'Только продаю'), ('barter', 'Одновременно покупаю другую')])
    phone = models.CharField(max_length=30,name='Номер телефона')
    whatsapp = models.CharField(max_length=30,name='Whatsapp')
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_total_cost(self):
        if self.promotion:
            return self.price + self.promotion.calculate_total_cost()
        return self.price

    def __str__(self):
        return self.headings

class RentLongAdvertisement(models.Model):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                    default='owner')
    type_of_deal = models.CharField(name='Тип сделки', max_length=40, default='Продажа')
    type_of_property = models.CharField(name='Тип недвижимости', max_length=50, default='Жилая')
    obj = models.CharField(name='Объект', max_length=100,
                           choices=[('flat', 'Квартира'), ('new_flat', 'Квартира в новостройке'),
                                    ('room', 'Комната'), ('part_flat', 'Доля в квартире'), ('house', 'Дом'),
                                    ('cottege', 'Коттедж'), ('tanhouse', 'Танхаус'), ('part_house', 'Часть дома'),
                                    ('spot', 'Участок')],
                           default='owner')
    address = models.CharField(name='Адресс', max_length=400)
    nearest_stop = models.CharField(name='Ближайшая остановка', max_length=400)
    minute_stop = models.CharField(name='Минут до остановки', max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')],
                                 default='afoot')
    floor = models.PositiveIntegerField()
    floors_house = models.PositiveIntegerField()
    number_flat = models.CharField(max_length=30, name='Номер квартиры')
    count_rooms = models.CharField(max_length=20, choices=[('Atelier', 'Студия'), ('1', '1'),
                                                          ('2', '2'), ('3', '3'), ('4', '4'),
                                                           ('5', '5'), ('6+', '6'), ('free_layout', 'Свободная планировка')])
    total_area = models.PositiveIntegerField(name='Общая площадь')
    living_area = models.PositiveIntegerField(name='Жилая площадь')
    kitchen_area = models.PositiveIntegerField(name='Кухня')
    property_type = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')])
    photo = models.ImageField(upload_to='images/')
    video = models.CharField(max_length=300,name='Видео')
    balconies = models.PositiveIntegerField(name='Балконы',default=0)
    loggia = models.PositiveIntegerField(name='Лоджия',default=0)
    view_from_window = models.CharField(max_length=30, choices=[('outside', 'На улицу'), ('into_the_courtyard', 'Во двор')])
    bathroom = models.PositiveIntegerField(name='Раздельный',default=0)
    bathroom_joint = models.PositiveIntegerField(name='Совмещенный',default=0)
    repair = models.CharField(max_length=70, choices=[('without_repair', 'Без ремонта'), ('cosmetic', 'Космитический'),
                                                      ('euro',"Евро"),('disigner', 'Дизайнерский')])
    elevators_passengers = models.PositiveIntegerField(name='Пассажирский',default=0)
    elevators_cargo = models.PositiveIntegerField(name='Грузовой',default=0)
    entrance = models.CharField(max_length=30, choices=[('ramp', 'Пандус'), ('garbage_chute', 'Мусоропровод')])
    parking = models.CharField(max_length=30, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'),
                                                       ('underground','Подземная'), ('in_roof','На крыше')])
    headings = models.CharField(max_length=100,name='Загаловок')
    description = models.TextField(name='Описание')
    rent_per_month = models.FloatField()
    shetchik = models.CharField(max_length=70, choices=[('owner', 'Собственник'), ('tenant', 'Арендатор')])
    prepayment = models.CharField(max_length=70, choices=[('for_month', 'За месяц'), ('1', '1'),
                                                      ('2',"2"),('3', '3'),('4+', '4+')])
    deposit = models.FloatField(blank=True,null=True)
    rental_period = models.CharField(max_length=70, choices=[('few_months', 'Несколько месяцев'), ('from_the_year', 'От года')])
    living_baby =  models.BooleanField()
    living_animal = models.BooleanField()
    phone = models.CharField(max_length=30,name='Номер телефона')
    dop_phone = models.CharField(max_length=30,name='Номер телефона',blank=True,null=True)
    communication_method = models.CharField(max_length=70, choices=[('calls_and_messages', 'Звонки и сообщения'), ('whatsapp', 'WhatsApp'), ('only_calls','Только звонки')])
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_total_cost(self):
        if self.promotion:
            return self.price + self.promotion.calculate_total_cost()
        return self.price

    def __str__(self):
        return self.headings

class RentDayAdvertisement(models.Model):
    pass