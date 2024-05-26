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
    cost_per_day = models.PositiveIntegerField()
    discount_7_days = models.FloatField(default=0.10)
    discount_14_days = models.FloatField(default=0.15)
    discount_30_days = models.FloatField(default=0.20)

    def __str__(self):
        return self.get_promotion_type_display()

class Builder(models.Model):
    name = models.CharField(max_length=100)



class BaseModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, name='Тип аккаунта' ,choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner')
    deal_type = models.CharField(name='Тип сделки' ,max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')])
    type_of_property = models.CharField(name = 'Жилая',max_length=50, choices=[('residential', 'Жилая'), ('commercial', 'Комерческая')])
    obj = models.CharField(name = 'Объект', max_length=100,
                           choices=[('flat', 'Квартира'), ('new_flat', 'Квартира в новостройке'),
                                    ('room','Комната'), ('part_flat','Доля в квартире'), ('house', 'Дом'),
                                    ('cottege','Коттедж'), ('tanhouse', 'Танхаус'), ('part_house', 'Часть дома'), ('spot','Участок')]
                          )
    address = models.CharField(name='Адресс',max_length=400)
    nearest_stop = models.CharField(name='Ближайшая остановка',max_length=400)
    minute_stop = models.CharField(name='Минут до остановки',max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')],
                                    default='afoot')
    count_rooms = models.CharField(max_length=20, choices=[('Atelier', 'Студия'), ('1', '1'),
                                                           ('2', '2'), ('3', '3'), ('4', '4'),
                                                           ('5', '5'), ('6+', '6'),
                                                           ('free_layout', 'Свободная планировка')])
    total_area = models.PositiveIntegerField(name='Общая площадь')
    living_area = models.PositiveIntegerField(name='Жилая площадь',blank=True,null=True)
    kitchen_area = models.PositiveIntegerField(name='Кухня',blank=True,null=True)
    property_type = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')])
    photo = models.ImageField(upload_to='images/')
    video = models.CharField(max_length=300, name='Видео',blank=True,null=True)
    headings = models.CharField(max_length=100, name='Загаловок')
    description = models.TextField(name='Описание')
    balconies = models.PositiveIntegerField(name='Балконы',default=0)
    loggia = models.PositiveIntegerField(name='Лоджия',default=0)
    view_from_window = models.CharField(max_length=30, choices=[('outside', 'На улицу'), ('into_the_courtyard', 'Во двор')],blank=True,null=True)
    bathroom = models.PositiveIntegerField(name='Раздельный',default=0)
    bathroom_joint = models.PositiveIntegerField(name='Совмещенный',default=0)
    repair = models.CharField(max_length=70, name='Ремонт' ,choices=[('without_repair', 'Без ремонта'), ('cosmetic', 'Космитический'),
                                                      ('euro',"Евро"),('disigner', 'Дизайнерский')],blank=True,null=True)
    elevators_passengers = models.PositiveIntegerField(name='Пассажирский',default=0)
    elevators_cargo = models.PositiveIntegerField(name='Грузовой',default=0)
    entrance = models.CharField(max_length=30, name='Подъезд' ,choices=[('ramp', 'Пандус'), ('garbage_chute', 'Мусоропровод')],blank=True,null=True)
    parking = models.CharField(max_length=30, name='Парковка' ,choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'),
                                                       ('underground','Подземная'), ('in_roof','На крыше')],blank=True,null=True)

    phone = models.CharField(max_length=30,name='Номер телефона')


class SaleResidential(BaseModel):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    floor = models.PositiveIntegerField(name='Этаж')
    floors_house = models.PositiveIntegerField('Всего этажей')
    number_flat = models.CharField(max_length=30, name='Номер квартиры', blank=True, null=True)
    age_build = models.PositiveIntegerField(name='Год постройки', blank=True,null=True)
    ceiling_height = models.PositiveIntegerField(name='Высота потолков',blank=True,null=True)
    type_house = models.CharField(name='Тип дома',max_length=100, choices=[
        ('brick','Кирпичный'),
        ('monolit','Монолитный'),
        ('panel','Панельный'),
        ('block','Блочный'),
        ('wood','Деревянный'),
    ])
    price = models.PositiveIntegerField(name='Цена')
    currency = models.CharField(name='Валюта',max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    is_ipoteka = models.BooleanField(default=False)
    how_sale = models.CharField(name='Как продаете',max_length=50, choices=[
        ('only_sale','Только продаю'),
        ('sale_another','Одновременно покупаю другую'),
    ])
    whatsapp = models.CharField(name='Whatsapp',max_length=300)
    promotion = models.ForeignKey('Promotion', on_delete=models.SET_NULL, null=True, blank=True)
class BaseSaleComerc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, name='Тип аккаунта' ,choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                    default='owner')
    deal_type = models.CharField(name='Тип сделки', max_length=100, choices=[('sale', 'Продажа'), ('rent', 'Аренда')])
    type_of_property = models.CharField(name='Жилая', max_length=50,
                                        choices=[('residential', 'Жилая'), ('commercial', 'Комерческая')])
    obj = models.CharField(name = 'Объект', max_length=100,
                           choices=[('ofice', 'Офис'), ('building', 'Здание'),
                                    ('retail_space','Торговая площадь'), ('free_place','Помещение свободного назначения'), ('production', 'Производство'),
                                    ('warehouse','Склад'), ('garage', 'Гараж'), ('business', 'Бизнес'), ('commer_land','Коммерческая земля')])

    address = models.CharField(name='Адрес',max_length=400)
    nearest_stop = models.CharField(name='Ближайшая остановка',max_length=400)
    minute_stop = models.CharField(name='Минут до остановки',max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')],
                                    default='afoot')

    number_nalog = models.CharField(max_length=100,name='Номер налоговой')
    total_area = models.PositiveIntegerField(name='Общая площадь')
    ceiling_height = models.PositiveIntegerField(name='Высота потолков',blank=True,null=True)
    floor = models.PositiveIntegerField(name='Этаж')
    floors_house = models.PositiveIntegerField('Всего этажей')
    ur_adress = models.CharField(max_length=200,name='',choices=[('provided ','Предоставляется'),('no_provided ','Не предоставляется')])
    room_busy = models.BooleanField(name = 'Занято')
    layout = models.CharField(max_length=30, name='Планировка',choices=[('open','Открытая'),('coridor','Коридор'),('cabinet','Кабинетная')])
    count_raint_touch = models.CharField(max_length=50, blank=True,null=True ,name='Кол-во мокрых точек',choices=[('no','Нет'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5 и больше')])
    electric = models.PositiveIntegerField(name='Электрическая мощность',blank=True,null=True)
    condition = models.CharField(name='Состояние',max_length=100, blank=True,null=True ,choices=[('office','Офисная отделка'), ('clean_ot','Под чистовую отделку'), ('cap_repair', 'Требутеся капитальный ремонт'),('cosmetic_repair','Требутеся косметический ремонт')])
    mebel = models.BooleanField(name='Мебель',default=False)
    access = models.CharField(max_length=30, name='Доступ', blank=True,null=True,choices=[('free','Свободный'),('propusk','Пропуская система')])
    parking = models.CharField(max_length=30, name='Паркинг' , blank=True,null=True,choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'),
                                                       ('underground','Подземная'), ('in_roof','На крыше')])
    numner_seats = models.PositiveIntegerField(name='Кол-во мест', blank=True,null=True)
    price_park = models.CharField(max_length=30, name='Планировка парковки', blank=True,null=True ,choices=[('paid','Платная'),('free','Бесплатная')])
    price_month = models.PositiveIntegerField(name='Стоимость парковки',blank=True,null=True)
    name_building = models.CharField(max_length=200, name='Название')
    age_build = models.PositiveIntegerField(name='Год постройки', blank=True,null=True)
    type_building = models.CharField(max_length=100,name='Тип здания', blank=True,null=True)
    klass_zd = models.CharField(max_length=3, blank=True,null=True ,name='Класс здания', choices=[('A', 'A'), ('A+', 'A+'),
                                                                            ('B', 'B'), ('B+', 'B+'),
                                                                            ('B-', 'B-'), ('C', 'C')])
    area_zd = models.PositiveIntegerField(name='Площадь здания', blank=True,null=True)
    region = models.PositiveIntegerField(name='Участок', blank=True,null=True)
    in_sobstven = models.BooleanField(name='В собсвтенноем',default=False)
    in_rent = models.BooleanField(name='В аренде',default=False)
    category = models.CharField(max_length=30,
                                choices=[('doing', 'Действующее'), ('project', 'Проект'), ('building', 'Строящееся')])
    developer = models.CharField(max_length=200, name='Девелопер', blank=True,null=True)
    upr_company = models.CharField(max_length=200, name='Управляющая компания', blank=True,null=True)
    ventilation = models.CharField(max_length=30, blank=True,null=True,
                                   choices=[('natural', 'Естественная'), ('supply', 'Приточная'), ('no', 'Нет')])
    conditioning = models.CharField(max_length=30, name='Кондиционирование', blank=True,null=True,
                                    choices=[('local', 'Местное'), ('center', 'Центральное'), ('no', 'Нет')])
    heating = models.CharField(max_length=30, name = 'Отопление',blank=True,null=True,choices=[('auto', 'Автономное'), ('center', 'Центральное'), ('no', 'Нет')])
    fire_stop = models.CharField(max_length=30, blank=True,null=True ,name='Система пожаротушения' ,choices=[('gidro', 'Гидратная'), ('sprinkler', 'Спринклерная'), ('powder', 'Порошковая'),('gas', 'Газовая'),('signal', 'Сигнализация'),
                                                         ('no', 'Нет')])
    auto_wish = models.BooleanField(name='Автомойка',default=False)
    auto_service = models.BooleanField(name='Автосервис',default=False)
    pharmacy = models.BooleanField(name='Аптека',default=False)
    atelier = models.BooleanField(name='Ателье одежды',default=False)
    bank = models.BooleanField(name='Бассейн',default=False)
    bufet = models.BooleanField(name = 'Буфет',default=False)
    sclad = models.BooleanField(name='Выставочно-складский комплекс',default=False)
    hotel = models.BooleanField(name='Гостиница',default=False)
    cafe = models.BooleanField(name='Кафе',default=False)
    tv_vinema = models.BooleanField(name='Кинотеатр',default=False)
    conference = models.BooleanField(name='Коференц-зал',default=False)
    med_center = models.BooleanField(name='Медецинский центр',default=False)
    mini_market = models.BooleanField(name='Минимаркет',default=False)
    notarial_contore = models.BooleanField(name='Нотариальная контора',default=False)
    otdel_bank = models.BooleanField(name='Отделение банка',default=False)
    park = models.BooleanField(name='Парк',default=False)
    restoran = models.BooleanField(name='Ресторан',default=False)
    beaty_salon = models.BooleanField(name='Салон красоты',default=False)
    sclad_place = models.BooleanField(name='Складское помещение',default=False)
    stolov = models.BooleanField(name='Столовая',default=False)
    supermarket = models.BooleanField(name='Супермаркет',default=False)
    torg_zona = models.BooleanField(name='Торговая зона',default=False)
    fitness = models.BooleanField(name='Фитнес-центр',default=False)
    central_recep = models.BooleanField(name='Центральная рецепция',default=False)
    photo = models.ImageField(upload_to='images/')
    video = models.CharField(max_length=300, name='Видео',blank=True,null=True)
    headings = models.CharField(max_length=100, name='Загаловок')
    description = models.TextField(name='Описание')

class BaseRent:
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, name='Тип аккаунта' ,choices=[('owner', 'Собственник'), ('agent', 'Агент')],
                                    default='owner')
    type_of_deal = models.CharField(name = 'Объект', max_length=100,
                           choices=[('sale','Продажа'),('rent','Аренда')] )
    type_of_property = models.CharField(name = 'Жилая',max_length=50, choices=[('residential', 'Жилая')])
    obj = models.CharField(name = 'Объект', max_length=100,
                           choices=[('flat', 'Квартира'),('room','Комната'), ('house', 'Дом'), ('place','Койко-место')]
                          )
    address = models.CharField(name='Адрес',max_length=400)
    nearest_stop = models.CharField(name='Ближайшая остановка',max_length=400)
    minute_stop = models.CharField(name='Минут до остановки',max_length=400)
    transport = models.CharField(max_length=20, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')],
                                    default='afoot')
    count_rooms = models.CharField(max_length=20, choices=[('Atelier', 'Студия'), ('1', '1'),
                                                           ('2', '2'), ('3', '3'), ('4', '4'),
                                                           ('5', '5'), ('6+', '6'),
                                                           ('free_layout', 'Свободная планировка')])
    total_area = models.PositiveIntegerField(name='Общая площадь')
    kitchen_area = models.PositiveIntegerField(name='Кухня',blank=True,null=True)
    property_type = models.CharField(max_length=30, choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')])
    photo = models.ImageField(upload_to='images/')
    video = models.CharField(max_length=300, name='Видео',blank=True,null=True)
    headings = models.CharField(max_length=100,name='Загаловок')
    description = models.TextField(name='Описание')
    phone = models.CharField(max_length=30,name='Номер телефона')



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





class RentLongAdvertisement(BaseModel):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    type_rent_long =  models.CharField(max_length=70, name='Тип аренды' ,choices=[('long', 'Длительно'), ('day', 'Посуточно')])
    floor = models.PositiveIntegerField(name = 'Этаж')
    floors_house = models.PositiveIntegerField(name = 'кол-во этажей')
    number_flat = models.CharField(max_length=30, name='Номер квартиры', blank=True, null=True)

    rent_per_month = models.PositiveIntegerField(name = 'Аренда в месяц')
    shetchik = models.CharField(max_length=70, name='Кто платит ЖКУ' ,choices=[('owner', 'Собственник'), ('tenant', 'Арендатор')])
    prepayment = models.CharField(max_length=70, name='Предоплата',choices=[('for_month', 'За месяц'), ('1', '1'),
                                                      ('2',"2"),('3', '3'),('4+', '4+')])
    deposit = models.PositiveIntegerField(name='Депозит',blank=True,null=True)
    rental_period = models.CharField(max_length=70, name = 'Срок аренды',choices=[('few_months', 'Несколько месяцев'), ('from_the_year', 'От года')])
    living_baby =  models.BooleanField(name='Жить с детьми',default=False)
    living_animal = models.BooleanField(name = 'Жить с животными',default=False)
    additional_phone = models.CharField(max_length=30,name='Дополнительный номер телефона',blank=True,null=True)  # Renamed to avoid conflict
    communication_method = models.CharField(max_length=70, name='Коммуникация' ,choices=[('calls_and_messages', 'Звонки и сообщения'), ('whatsapp', 'WhatsApp'), ('only_calls','Только звонки')])
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    without_mebel = models.BooleanField(name='Без мебели',default=False,blank=True,null=True)
    mebel_kitchen = models.BooleanField(name='На кухне',default=False,blank=True,null=True)
    mebel_rooms = models.BooleanField(name = 'В комнатах',default=False,blank=True,null=True)
    bathroom_vanna = models.BooleanField(name='Ванная',default=False,blank=True,null=True)
    bathroom_doosh = models.BooleanField(name='Душевая',default=False,blank=True,null=True)
    split = models.BooleanField(name='Сплит',default=False,blank=True,null=True)
    holodilnik = models.BooleanField(name='Холодильник',default=False,blank=True,null=True)
    tv = models.BooleanField(name='ТВ',default=False,blank=True,null=True)
    posud_car = models.BooleanField(name='Посудомоячная мащина',default=False,blank=True,null=True)
    stiral_car = models.BooleanField(name='Стиральная машина',default=False,blank=True,null=True)
    internet = models.BooleanField(name='Интернет',default=False,blank=True,null=True)
    phone_house = models.BooleanField(name='Домашний телефон',default=False,blank=True,null=True)


    def __str__(self):
        return self.headings

class RentDayAdvertisement(BaseRent):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    type_rent_long =  models.CharField(max_length=70, name='Тип аренды' ,choices=[('long', 'Длительно'), ('day', 'Посуточно')])
    price_day = models.PositiveIntegerField(name='Цена за сутки')
    deposit = models.PositiveIntegerField(name='Залог',blank=True,null=True)
    currency_month = models.CharField(name='Валюта для аренды',max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    currency_deposit= models.CharField(name='Валюта для залога',max_length=3, choices=CURRENCY_CHOICES, default='mzn')
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    without_mebel = models.BooleanField(name='Без мебели',default=False,blank=True,null=True)
    mebel_kitchen = models.BooleanField(name='На кухне',default=False,blank=True,null=True)
    mebel_rooms = models.BooleanField(name = 'В комнатах',default=False,blank=True,null=True)
    bathroom_vanna = models.BooleanField(name='Ванная',default=False,blank=True,null=True)
    bathroom_doosh = models.BooleanField(name='Душевая',default=False,blank=True,null=True)
    split = models.BooleanField(name='Сплит',default=False,blank=True,null=True)
    holodilnik = models.BooleanField(name='Холодильник',default=False,blank=True,null=True)
    tv = models.BooleanField(name='ТВ',default=False,blank=True,null=True)
    posud_car = models.BooleanField(name='Посудомоячная мащина',default=False,blank=True,null=True)
    stiral_car = models.BooleanField(name='Стиральная машина',default=False,blank=True,null=True)
    internet = models.BooleanField(name='Интернет',default=False,blank=True,null=True)
    phone_house = models.BooleanField(name='Домашний телефон',default=False,blank=True,null=True)



class SaleCommercialAdvertisement(BaseSaleComerc):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    currency_all = models.CharField(max_length=3, name='Валюта за все' ,choices=CURRENCY_CHOICES, default='mzn')
    price_all = models.PositiveIntegerField(name='Цена за все')
    currency_kv_m = models.CharField(max_length=3, name='Валюта за кв м' ,choices=CURRENCY_CHOICES, default='mzn')
    price_kv_m = models.PositiveIntegerField(name='Цена за кв м')
    is_nalog = models.CharField(max_length=70, name='Налог', choices=[('nds_on','Ндс включен'),('nds_off','Ндс не облегается'),
                                                                      ('just_nalog','Упрощенная налогобложения')])
    bonus_agent = models.CharField(max_length=70, name='Бонус агенту', choices=[('no','Нет'),('fix_sum','Фиксированная сумма'),
                                                                      ('procent','Процент от сделки')])
    phone = models.CharField(max_length=30,name='Телефон')
    dop_phone = models.CharField(max_length=30,name='Доп телефон')
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)


class RentCommercialAdvertisement(BaseSaleComerc):
    CURRENCY_CHOICES = [
        ('mzn', 'MZN'),
        ('usd', 'Доллар'),
        ('eur', 'Евро'),
    ]
    currency_month_kv_m = models.CharField(max_length=3, name='Валюта в месяц  за м^2',choices=CURRENCY_CHOICES, default='mzn')
    rent_month_kv_m  = models.PositiveIntegerField(name='Аренда в месяц  за м^2')
    currency_kv_m_year = models.CharField(max_length=3, name='Валюта в год за м^2' ,choices=CURRENCY_CHOICES, default='mzn')
    price_kv_m_year = models.PositiveIntegerField(name='Аренда в год за м^2')
    currency_rent_month = models.CharField(max_length=3, name='Валюта аренда за месяц', choices=CURRENCY_CHOICES, default='mzn')
    rent_month = models.PositiveIntegerField(name='Аренда за месяц ')
    is_nalog = models.CharField(max_length=70, name='Налог',
                                choices=[('nds_on', 'Ндс включен'), ('nds_off', 'Ндс не облегается'),
                                         ('just_nalog', 'Упрощенная налогобложения')])
    is_communal = models.BooleanField(default=False,name='Комунальный платежи')
    is_exploitation = models.BooleanField(default=False,name='Экспаутационные  расходы')

    type_rent = models.CharField(name='Тип аренды',max_length=30,choices=[('direct_rental','Прямая аренда',('subrent','Субаренда'))])
    min_rent_period = models.PositiveIntegerField('Минимальный срок аренды')
    rent_holidays = models.BooleanField(default=False,name='Арендные каникулы')
    security_deposit = models.PositiveIntegerField(name='Обеспечительный платеж')
    security_deposit_currency = models.CharField(max_length=3, name='Валюта за обеспечительный платеж'  ,choices=CURRENCY_CHOICES, default='mzn')
    prepayment = models.CharField(name='Предоплата',max_length=30, choices=[
        ('4','4 мес'),
        ('5','5 мес')
        ('6','6 мес')
        ('7','7 мес')
        ('8','8 мес')
        ('9','9 мес')
        ('10','10 мес')
        ('11','11 мес')
        ('year','Год')
    ])
    bonus_agent = models.CharField(max_length=70, name='Бонус агенту', choices=[('no','Нет'),('fix_sum','Фиксированная сумма'),
                                                                      ('procent','Процент от сделки')])
    phone = models.CharField(max_length=30,name='Телефон')
    dop_phone = models.CharField(max_length=30,name='Доп телефон')
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)