# Generated by Django 5.0.6 on 2024-06-25 23:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatemaster', '0012_infastructure_alter_advertisement_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='infastructure',
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='promotion',
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='user',
        ),
        migrations.CreateModel(
            name='RentCommercialAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner', max_length=20)),
                ('deal_type', models.CharField(choices=[('sale', 'Продажа'), ('rent', 'Аренда')], max_length=100)),
                ('type_of_property', models.CharField(choices=[('residential', 'Жилая'), ('commercial', 'Коммерческая')], max_length=50)),
                ('obj', models.CharField(choices=[('office', 'Офис'), ('building', 'Здание'), ('retail_space', 'Торговая площадь'), ('free_place', 'Помещение свободного назначения'), ('production', 'Производство'), ('warehouse', 'Склад'), ('garage', 'Гараж'), ('business', 'Бизнес'), ('commercial_land', 'Коммерческая земля')], max_length=100)),
                ('address', models.CharField(max_length=400)),
                ('nearest_stop', models.CharField(max_length=400)),
                ('minute_stop', models.CharField(max_length=400)),
                ('transport', models.CharField(choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot', max_length=20)),
                ('number_nalog', models.CharField(max_length=100)),
                ('total_area', models.PositiveIntegerField()),
                ('ceiling_height', models.PositiveIntegerField(blank=True, null=True)),
                ('floor', models.PositiveIntegerField()),
                ('floors_house', models.PositiveIntegerField()),
                ('ur_address', models.CharField(choices=[('provided', 'Предоставляется'), ('not_provided', 'Не предоставляется')], max_length=200)),
                ('room_busy', models.BooleanField(default=False)),
                ('layout', models.CharField(choices=[('open', 'Открытая'), ('corridor', 'Коридор'), ('cabinet', 'Кабинетная')], max_length=30)),
                ('count_raint_touch', models.CharField(blank=True, choices=[('no', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 и больше')], max_length=50, null=True)),
                ('electric', models.PositiveIntegerField(blank=True, null=True)),
                ('condition', models.CharField(blank=True, choices=[('office', 'Офисная отделка'), ('clean_ot', 'Под чистовую отделку'), ('cap_repair', 'Требуется капитальный ремонт'), ('cosmetic_repair', 'Требуется косметический ремонт')], max_length=100, null=True)),
                ('mebel', models.BooleanField(default=False)),
                ('access', models.CharField(blank=True, choices=[('free', 'Свободный'), ('propusk', 'Пропускная система')], max_length=30, null=True)),
                ('parking', models.CharField(blank=True, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')], max_length=30, null=True)),
                ('numner_seats', models.PositiveIntegerField(blank=True, null=True)),
                ('price_park', models.CharField(blank=True, choices=[('paid', 'Платная'), ('free', 'Бесплатная')], max_length=30, null=True)),
                ('price_month', models.PositiveIntegerField(blank=True, null=True)),
                ('name_building', models.CharField(max_length=200)),
                ('age_build', models.PositiveIntegerField(blank=True, null=True)),
                ('type_building', models.CharField(blank=True, max_length=100, null=True)),
                ('klass_zd', models.CharField(blank=True, choices=[('A', 'A'), ('A+', 'A+'), ('B', 'B'), ('B+', 'B+'), ('B-', 'B-'), ('C', 'C')], max_length=3, null=True)),
                ('area_zd', models.PositiveIntegerField(blank=True, null=True)),
                ('region', models.PositiveIntegerField(blank=True, null=True)),
                ('in_sobstven', models.BooleanField(default=False)),
                ('in_rent', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('doing', 'Действующее'), ('project', 'Проект'), ('building', 'Строящееся')], max_length=30)),
                ('developer', models.CharField(blank=True, max_length=200, null=True)),
                ('upr_company', models.CharField(blank=True, max_length=200, null=True)),
                ('ventilation', models.CharField(blank=True, choices=[('natural', 'Естественная'), ('supply', 'Приточная'), ('no', 'Нет')], max_length=30, null=True)),
                ('conditioning', models.CharField(blank=True, choices=[('local', 'Местное'), ('center', 'Центральное'), ('no', 'Нет')], max_length=30, null=True)),
                ('heating', models.CharField(blank=True, choices=[('auto', 'Автономное'), ('center', 'Центральное'), ('no', 'Нет')], max_length=30, null=True)),
                ('fire_stop', models.CharField(blank=True, choices=[('gidro', 'Гидрантная'), ('sprinkler', 'Спринклерная'), ('powder', 'Порошковая'), ('gas', 'Газовая'), ('signal', 'Сигнализация'), ('no', 'Нет')], max_length=30, null=True)),
                ('auto_wish', models.BooleanField(default=False)),
                ('auto_service', models.BooleanField(default=False)),
                ('pharmacy', models.BooleanField(default=False)),
                ('atelier', models.BooleanField(default=False)),
                ('bank', models.BooleanField(default=False)),
                ('bufet', models.BooleanField(default=False)),
                ('sclad', models.BooleanField(default=False)),
                ('hotel', models.BooleanField(default=False)),
                ('cafe', models.BooleanField(default=False)),
                ('tv_vinema', models.BooleanField(default=False)),
                ('conference', models.BooleanField(default=False)),
                ('med_center', models.BooleanField(default=False)),
                ('mini_market', models.BooleanField(default=False)),
                ('notarial_contore', models.BooleanField(default=False)),
                ('otdel_bank', models.BooleanField(default=False)),
                ('park', models.BooleanField(default=False)),
                ('restoran', models.BooleanField(default=False)),
                ('beaty_salon', models.BooleanField(default=False)),
                ('sclad_place', models.BooleanField(default=False)),
                ('stolov', models.BooleanField(default=False)),
                ('supermarket', models.BooleanField(default=False)),
                ('torg_zona', models.BooleanField(default=False)),
                ('fitness', models.BooleanField(default=False)),
                ('central_recep', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, upload_to='images/')),
                ('video', models.CharField(blank=True, max_length=300, null=True)),
                ('headings', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('currency_month_kv_m', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('rent_month_kv_m', models.PositiveIntegerField()),
                ('currency_kv_m_year', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('price_kv_m_year', models.PositiveIntegerField()),
                ('currency_rent_month', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('rent_month', models.PositiveIntegerField()),
                ('is_nalog', models.CharField(choices=[('nds_on', 'НДС включен'), ('nds_off', 'НДС не облагается'), ('just_nalog', 'Упрощенная налогобложение')], max_length=70)),
                ('is_communal', models.BooleanField(default=False)),
                ('is_exploitation', models.BooleanField(default=False)),
                ('type_rent', models.CharField(choices=[('direct_rental', 'Прямая аренда'), ('subrent', 'Субаренда')], max_length=30)),
                ('min_rent_period', models.PositiveIntegerField()),
                ('rent_holidays', models.BooleanField(default=False)),
                ('security_deposit', models.PositiveIntegerField()),
                ('security_deposit_currency', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('prepayment', models.CharField(choices=[('4', '4 мес'), ('5', '5 мес'), ('6', '6 мес'), ('7', '7 мес'), ('8', '8 мес'), ('9', '9 мес'), ('10', '10 мес'), ('11', '11 мес'), ('year', 'Год')], max_length=30)),
                ('bonus_agent', models.CharField(choices=[('no', 'Нет'), ('fix_sum', 'Фиксированная сумма'), ('procent', 'Процент от сделки')], max_length=70)),
                ('phone', models.CharField(max_length=30)),
                ('dop_phone', models.CharField(max_length=30)),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estatemaster.promotion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Комерческие аренды',
                'verbose_name_plural': 'Комерческая аренда',
            },
        ),
        migrations.CreateModel(
            name='RentDayAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner', max_length=20)),
                ('type_of_deal', models.CharField(choices=[('sale', 'Продажа'), ('rent', 'Аренда')], max_length=100)),
                ('type_of_property', models.CharField(choices=[('residential', 'Жилая')], max_length=50)),
                ('obj', models.CharField(choices=[('flat', 'Квартира'), ('room', 'Комната'), ('house', 'Дом'), ('place', 'Койко-место')], max_length=100)),
                ('address', models.CharField(max_length=400)),
                ('nearest_stop', models.CharField(max_length=400)),
                ('minute_stop', models.CharField(max_length=400)),
                ('transport', models.CharField(choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot', max_length=20)),
                ('count_rooms', models.CharField(choices=[('Atelier', 'Студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6+', '6'), ('free_layout', 'Свободная планировка')], max_length=20)),
                ('total_area', models.PositiveIntegerField()),
                ('kitchen_area', models.PositiveIntegerField(blank=True, null=True)),
                ('property_type', models.CharField(choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')], max_length=30)),
                ('photo', models.ImageField(upload_to='images/')),
                ('video', models.CharField(blank=True, max_length=300, null=True)),
                ('headings', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('phone', models.CharField(max_length=30)),
                ('type_rent_long', models.CharField(choices=[('long', 'Длительно'), ('day', 'Посуточно')], max_length=70)),
                ('price_day', models.PositiveIntegerField()),
                ('deposit', models.PositiveIntegerField(blank=True, null=True)),
                ('currency_month', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('currency_deposit', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('without_mebel', models.BooleanField(blank=True, default=False, null=True)),
                ('mebel_kitchen', models.BooleanField(blank=True, default=False, null=True)),
                ('mebel_rooms', models.BooleanField(blank=True, default=False, null=True)),
                ('bathroom_vanna', models.BooleanField(blank=True, default=False, null=True)),
                ('bathroom_doosh', models.BooleanField(blank=True, default=False, null=True)),
                ('split', models.BooleanField(blank=True, default=False, null=True)),
                ('holodilnik', models.BooleanField(blank=True, default=False, null=True)),
                ('tv', models.BooleanField(blank=True, default=False, null=True)),
                ('posud_car', models.BooleanField(blank=True, default=False, null=True)),
                ('stiral_car', models.BooleanField(blank=True, default=False, null=True)),
                ('internet', models.BooleanField(blank=True, default=False, null=True)),
                ('phone_house', models.BooleanField(blank=True, default=False, null=True)),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estatemaster.promotion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Аренда посуточная продажи',
                'verbose_name_plural': 'Аренда посуточная продажа',
            },
        ),
        migrations.CreateModel(
            name='RentLongAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner', max_length=20)),
                ('deal_type', models.CharField(choices=[('sale', 'Продажа'), ('rent', 'Аренда')], max_length=100)),
                ('type_of_property', models.CharField(choices=[('residential', 'Жилая'), ('commercial', 'Коммерческая')], max_length=50)),
                ('obj', models.CharField(choices=[('flat', 'Квартира'), ('new_flat', 'Квартира в новостройке'), ('room', 'Комната'), ('part_flat', 'Доля в квартире'), ('house', 'Дом'), ('cottage', 'Коттедж'), ('townhouse', 'Таунхаус'), ('part_house', 'Часть дома'), ('spot', 'Участок')], max_length=100)),
                ('address', models.CharField(max_length=400)),
                ('nearest_stop', models.CharField(max_length=400)),
                ('minute_stop', models.CharField(max_length=400)),
                ('transport', models.CharField(choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot', max_length=20)),
                ('count_rooms', models.CharField(choices=[('Atelier', 'Студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6+', '6'), ('free_layout', 'Свободная планировка')], max_length=20)),
                ('total_area', models.PositiveIntegerField()),
                ('living_area', models.PositiveIntegerField(blank=True, null=True)),
                ('kitchen_area', models.PositiveIntegerField(blank=True, null=True)),
                ('property_type', models.CharField(choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')], max_length=30)),
                ('photo', models.ImageField(blank=True, upload_to='images/')),
                ('video', models.CharField(blank=True, max_length=300, null=True)),
                ('headings', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('balconies', models.PositiveIntegerField(default=0)),
                ('loggia', models.PositiveIntegerField(default=0)),
                ('view_from_window', models.CharField(blank=True, choices=[('outside', 'На улицу'), ('into_the_courtyard', 'Во двор')], max_length=30, null=True)),
                ('bathroom', models.PositiveIntegerField(default=0)),
                ('bathroom_joint', models.PositiveIntegerField(default=0)),
                ('repair', models.CharField(blank=True, choices=[('without_repair', 'Без ремонта'), ('cosmetic', 'Косметический'), ('euro', 'Евро'), ('designer', 'Дизайнерский')], max_length=70, null=True)),
                ('elevators_passengers', models.PositiveIntegerField(default=0)),
                ('elevators_cargo', models.PositiveIntegerField(default=0)),
                ('entrance', models.CharField(blank=True, choices=[('ramp', 'Пандус'), ('garbage_chute', 'Мусоропровод')], max_length=30, null=True)),
                ('parking', models.CharField(blank=True, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')], max_length=30, null=True)),
                ('phone', models.CharField(max_length=30)),
                ('type_rent_long', models.CharField(choices=[('long', 'Длительно'), ('day', 'Посуточно')], max_length=70)),
                ('floor', models.PositiveIntegerField()),
                ('floors_house', models.PositiveIntegerField()),
                ('number_flat', models.CharField(blank=True, max_length=30, null=True)),
                ('rent_per_month', models.PositiveIntegerField()),
                ('shetchik', models.CharField(choices=[('owner', 'Собственник'), ('tenant', 'Арендатор')], max_length=70)),
                ('prepayment', models.CharField(choices=[('for_month', 'За месяц'), ('1', '1'), ('2', '2'), ('3', '3'), ('4+', '4+')], max_length=70)),
                ('deposit', models.PositiveIntegerField(blank=True, null=True)),
                ('rental_period', models.CharField(choices=[('few_months', 'Несколько месяцев'), ('from_the_year', 'От года')], max_length=70)),
                ('living_baby', models.BooleanField(default=False)),
                ('living_animal', models.BooleanField(default=False)),
                ('additional_phone', models.CharField(blank=True, max_length=30, null=True)),
                ('communication_method', models.CharField(choices=[('calls_and_messages', 'Звонки и сообщения'), ('whatsapp', 'WhatsApp'), ('only_calls', 'Только звонки')], max_length=70)),
                ('without_mebel', models.BooleanField(blank=True, default=False, null=True)),
                ('mebel_kitchen', models.BooleanField(blank=True, default=False, null=True)),
                ('mebel_rooms', models.BooleanField(blank=True, default=False, null=True)),
                ('bathroom_vanna', models.BooleanField(blank=True, default=False, null=True)),
                ('bathroom_doosh', models.BooleanField(blank=True, default=False, null=True)),
                ('split', models.BooleanField(blank=True, default=False, null=True)),
                ('holodilnik', models.BooleanField(blank=True, default=False, null=True)),
                ('tv', models.BooleanField(blank=True, default=False, null=True)),
                ('posud_car', models.BooleanField(blank=True, default=False, null=True)),
                ('stiral_car', models.BooleanField(blank=True, default=False, null=True)),
                ('internet', models.BooleanField(blank=True, default=False, null=True)),
                ('phone_house', models.BooleanField(blank=True, default=False, null=True)),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estatemaster.promotion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Аренда длятельная продажи',
                'verbose_name_plural': 'Аренда длитальеная продажа',
            },
        ),
        migrations.CreateModel(
            name='SaleCommercialAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner', max_length=20)),
                ('deal_type', models.CharField(choices=[('sale', 'Продажа'), ('rent', 'Аренда')], max_length=100)),
                ('type_of_property', models.CharField(choices=[('residential', 'Жилая'), ('commercial', 'Коммерческая')], max_length=50)),
                ('obj', models.CharField(choices=[('office', 'Офис'), ('building', 'Здание'), ('retail_space', 'Торговая площадь'), ('free_place', 'Помещение свободного назначения'), ('production', 'Производство'), ('warehouse', 'Склад'), ('garage', 'Гараж'), ('business', 'Бизнес'), ('commercial_land', 'Коммерческая земля')], max_length=100)),
                ('address', models.CharField(max_length=400)),
                ('nearest_stop', models.CharField(max_length=400)),
                ('minute_stop', models.CharField(max_length=400)),
                ('transport', models.CharField(choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot', max_length=20)),
                ('number_nalog', models.CharField(max_length=100)),
                ('total_area', models.PositiveIntegerField()),
                ('ceiling_height', models.PositiveIntegerField(blank=True, null=True)),
                ('floor', models.PositiveIntegerField()),
                ('floors_house', models.PositiveIntegerField()),
                ('ur_address', models.CharField(choices=[('provided', 'Предоставляется'), ('not_provided', 'Не предоставляется')], max_length=200)),
                ('room_busy', models.BooleanField(default=False)),
                ('layout', models.CharField(choices=[('open', 'Открытая'), ('corridor', 'Коридор'), ('cabinet', 'Кабинетная')], max_length=30)),
                ('count_raint_touch', models.CharField(blank=True, choices=[('no', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 и больше')], max_length=50, null=True)),
                ('electric', models.PositiveIntegerField(blank=True, null=True)),
                ('condition', models.CharField(blank=True, choices=[('office', 'Офисная отделка'), ('clean_ot', 'Под чистовую отделку'), ('cap_repair', 'Требуется капитальный ремонт'), ('cosmetic_repair', 'Требуется косметический ремонт')], max_length=100, null=True)),
                ('mebel', models.BooleanField(default=False)),
                ('access', models.CharField(blank=True, choices=[('free', 'Свободный'), ('propusk', 'Пропускная система')], max_length=30, null=True)),
                ('parking', models.CharField(blank=True, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')], max_length=30, null=True)),
                ('numner_seats', models.PositiveIntegerField(blank=True, null=True)),
                ('price_park', models.CharField(blank=True, choices=[('paid', 'Платная'), ('free', 'Бесплатная')], max_length=30, null=True)),
                ('price_month', models.PositiveIntegerField(blank=True, null=True)),
                ('name_building', models.CharField(max_length=200)),
                ('age_build', models.PositiveIntegerField(blank=True, null=True)),
                ('type_building', models.CharField(blank=True, max_length=100, null=True)),
                ('klass_zd', models.CharField(blank=True, choices=[('A', 'A'), ('A+', 'A+'), ('B', 'B'), ('B+', 'B+'), ('B-', 'B-'), ('C', 'C')], max_length=3, null=True)),
                ('area_zd', models.PositiveIntegerField(blank=True, null=True)),
                ('region', models.PositiveIntegerField(blank=True, null=True)),
                ('in_sobstven', models.BooleanField(default=False)),
                ('in_rent', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('doing', 'Действующее'), ('project', 'Проект'), ('building', 'Строящееся')], max_length=30)),
                ('developer', models.CharField(blank=True, max_length=200, null=True)),
                ('upr_company', models.CharField(blank=True, max_length=200, null=True)),
                ('ventilation', models.CharField(blank=True, choices=[('natural', 'Естественная'), ('supply', 'Приточная'), ('no', 'Нет')], max_length=30, null=True)),
                ('conditioning', models.CharField(blank=True, choices=[('local', 'Местное'), ('center', 'Центральное'), ('no', 'Нет')], max_length=30, null=True)),
                ('heating', models.CharField(blank=True, choices=[('auto', 'Автономное'), ('center', 'Центральное'), ('no', 'Нет')], max_length=30, null=True)),
                ('fire_stop', models.CharField(blank=True, choices=[('gidro', 'Гидрантная'), ('sprinkler', 'Спринклерная'), ('powder', 'Порошковая'), ('gas', 'Газовая'), ('signal', 'Сигнализация'), ('no', 'Нет')], max_length=30, null=True)),
                ('auto_wish', models.BooleanField(default=False)),
                ('auto_service', models.BooleanField(default=False)),
                ('pharmacy', models.BooleanField(default=False)),
                ('atelier', models.BooleanField(default=False)),
                ('bank', models.BooleanField(default=False)),
                ('bufet', models.BooleanField(default=False)),
                ('sclad', models.BooleanField(default=False)),
                ('hotel', models.BooleanField(default=False)),
                ('cafe', models.BooleanField(default=False)),
                ('tv_vinema', models.BooleanField(default=False)),
                ('conference', models.BooleanField(default=False)),
                ('med_center', models.BooleanField(default=False)),
                ('mini_market', models.BooleanField(default=False)),
                ('notarial_contore', models.BooleanField(default=False)),
                ('otdel_bank', models.BooleanField(default=False)),
                ('park', models.BooleanField(default=False)),
                ('restoran', models.BooleanField(default=False)),
                ('beaty_salon', models.BooleanField(default=False)),
                ('sclad_place', models.BooleanField(default=False)),
                ('stolov', models.BooleanField(default=False)),
                ('supermarket', models.BooleanField(default=False)),
                ('torg_zona', models.BooleanField(default=False)),
                ('fitness', models.BooleanField(default=False)),
                ('central_recep', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, upload_to='images/')),
                ('video', models.CharField(blank=True, max_length=300, null=True)),
                ('headings', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('currency_all', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('price_all', models.PositiveIntegerField()),
                ('currency_kv_m', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('price_kv_m', models.PositiveIntegerField()),
                ('is_nalog', models.CharField(choices=[('nds_on', 'НДС включен'), ('nds_off', 'НДС не облагается'), ('just_nalog', 'Упрощенная налогобложение')], max_length=70)),
                ('bonus_agent', models.CharField(choices=[('no', 'Нет'), ('fix_sum', 'Фиксированная сумма'), ('procent', 'Процент от сделки')], max_length=70)),
                ('phone', models.CharField(max_length=30)),
                ('dop_phone', models.CharField(max_length=30)),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estatemaster.promotion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Комерческие продажи',
                'verbose_name_plural': 'Комерческая продажа',
            },
        ),
        migrations.CreateModel(
            name='SaleResidential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner', max_length=20)),
                ('deal_type', models.CharField(choices=[('sale', 'Продажа'), ('rent', 'Аренда')], max_length=100)),
                ('type_of_property', models.CharField(choices=[('residential', 'Жилая'), ('commercial', 'Комерческая')], max_length=50)),
                ('obj', models.CharField(choices=[('flat', 'Квартира'), ('new_flat', 'Квартира в новостройке'), ('room', 'Комната'), ('part_flat', 'Доля в квартире'), ('house', 'Дом'), ('cottage', 'Коттедж'), ('townhouse', 'Таунхаус'), ('part_house', 'Часть дома'), ('spot', 'Участок')], max_length=100)),
                ('address', models.CharField(max_length=400)),
                ('nearest_stop', models.CharField(max_length=400)),
                ('minute_stop', models.CharField(max_length=400)),
                ('transport', models.CharField(choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot', max_length=20)),
                ('count_rooms', models.CharField(choices=[('Atelier', 'Студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6+', '6'), ('free_layout', 'Свободная планировка')], max_length=20)),
                ('total_area', models.PositiveIntegerField()),
                ('living_area', models.PositiveIntegerField(blank=True, null=True)),
                ('kitchen_area', models.PositiveIntegerField(blank=True, null=True)),
                ('property_type', models.CharField(choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')], max_length=30)),
                ('photo', models.ImageField(blank=True, upload_to='images/')),
                ('video', models.CharField(blank=True, max_length=300, null=True)),
                ('headings', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('balconies', models.PositiveIntegerField(default=0)),
                ('loggia', models.PositiveIntegerField(default=0)),
                ('view_from_window', models.CharField(blank=True, choices=[('outside', 'На улицу'), ('into_the_courtyard', 'Во двор')], max_length=30, null=True)),
                ('bathroom', models.PositiveIntegerField(default=0)),
                ('bathroom_joint', models.PositiveIntegerField(default=0)),
                ('repair', models.CharField(blank=True, choices=[('without_repair', 'Без ремонта'), ('cosmetic', 'Косметический'), ('euro', 'Евро'), ('designer', 'Дизайнерский')], max_length=70, null=True)),
                ('elevators_passengers', models.PositiveIntegerField(default=0)),
                ('elevators_cargo', models.PositiveIntegerField(default=0)),
                ('entrance', models.CharField(blank=True, choices=[('ramp', 'Пандус'), ('garbage_chute', 'Мусоропровод')], max_length=30, null=True)),
                ('parking', models.CharField(blank=True, choices=[('ground', 'Наземная'), ('multilevel', 'Многоуровневая'), ('underground', 'Подземная'), ('in_roof', 'На крыше')], max_length=30, null=True)),
                ('phone', models.CharField(max_length=30)),
                ('floor', models.PositiveIntegerField()),
                ('floors_house', models.PositiveIntegerField()),
                ('number_flat', models.CharField(blank=True, max_length=30, null=True)),
                ('age_build', models.PositiveIntegerField(blank=True, null=True)),
                ('ceiling_height', models.PositiveIntegerField(blank=True, null=True)),
                ('type_house', models.CharField(choices=[('brick', 'Кирпичный'), ('monolit', 'Монолитный'), ('panel', 'Панельный'), ('block', 'Блочный'), ('wood', 'Деревянный')], max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('currency', models.CharField(choices=[('mzn', 'MZN'), ('usd', 'Доллар'), ('eur', 'Евро')], default='mzn', max_length=3)),
                ('how_sale', models.CharField(choices=[('only_sale', 'Только продаю'), ('sale_another', 'Одновременно покупаю другую')], max_length=50)),
                ('whatsapp', models.CharField(max_length=300)),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estatemaster.promotion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Жилые прожажи',
                'verbose_name_plural': 'Жилая продажа',
            },
        ),
        migrations.DeleteModel(
            name='Infastructure',
        ),
        migrations.DeleteModel(
            name='Advertisement',
        ),
    ]
