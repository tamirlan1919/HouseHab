# Generated by Django 5.1 on 2024-08-12 17:09

import django.db.models.deletion
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatemaster', '0021_alter_rentlongadvertisement_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='account_type',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='bathroom_doosh',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='bathroom_vanna',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='count_rooms',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='currency_deposit',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='currency_month',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='holodilnik',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='internet',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='mebel_kitchen',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='mebel_rooms',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='phone_house',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='posud_car',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='price_day',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='property_type',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='split',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='stiral_car',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='tv',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='type_of_deal',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='type_of_property',
        ),
        migrations.RemoveField(
            model_name='rentdayadvertisement',
            name='without_mebel',
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='accountType',
            field=models.CharField(blank=True, choices=[('owner', 'Собственник'), ('agent', 'Агент')], default='owner', max_length=20),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='additional_phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='bathroom_choice',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('bath', 'Ванна'), ('shower', 'Душевая кабина')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='communication',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('internet', 'Интернет'), ('phone', 'Телефон')], max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='daily_price',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Цена за сутки'),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='daily_price_currency',
            field=models.CharField(blank=True, choices=[('mzn', 'MZN'), ('usd', 'USD'), ('eur', 'EUR')], default='mzn', max_length=3),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='dealType',
            field=models.CharField(blank=True, choices=[('sale', 'Продажа'), ('rent', 'Аренда')], default='sale', max_length=100),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='deposit_currency',
            field=models.CharField(blank=True, choices=[('mzn', 'MZN'), ('usd', 'USD'), ('eur', 'EUR')], default='mzn', max_length=3),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='estateType',
            field=models.CharField(blank=True, choices=[('residential', 'Жилая')], default='residential', max_length=50),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='floor',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='floors_house',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='furniture',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('no_furniture', 'Без мебели'), ('kitchen', 'На кухне'), ('rooms', 'В комнатах')], max_length=26, null=True),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='guest_count',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='living_conditions',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('children_allowed', 'Можно с детьми'), ('pets_allowed', 'Можно с животными')], max_length=29, null=True, verbose_name='Условия проживания'),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='new_or_no',
            field=models.CharField(blank=True, choices=[('second', 'Вторичка'), ('new', 'Новостройка')], default='second', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='number_flat',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='propertyType',
            field=models.CharField(blank=True, choices=[('flat', 'Квартира'), ('apartment', 'Апартаменты')], max_length=30),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='roomsNumber',
            field=models.CharField(blank=True, choices=[('Atelier', 'Студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6+', '6'), ('free_layout', 'Свободная планировка')], max_length=20),
        ),
        migrations.AddField(
            model_name='rentdayadvertisement',
            name='tech',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('ac', 'Кондиционер'), ('fridge', 'Холодильник'), ('tv', 'Телевизор'), ('dishwasher', 'Посудомоечная машина'), ('washing_machine', 'Стиральная машина')], max_length=39, null=True),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='address',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='deposit',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Залог'),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='headings',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='kitchen_area',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='minute_stop',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='nearest_stop',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='obj',
            field=models.CharField(blank=True, choices=[('flat', 'Квартира'), ('room', 'Комната'), ('house', 'Дом'), ('place', 'Койко-место')], max_length=100),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='phone',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='photo',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estatemaster.location'),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='total_area',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='transport',
            field=models.CharField(blank=True, choices=[('afoot', 'Пешком'), ('car', 'Транспорт')], default='afoot', max_length=20),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='type_rent_long',
            field=models.CharField(blank=True, choices=[('long', 'Длительно'), ('day', 'Посуточно')], default='day', max_length=70),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]