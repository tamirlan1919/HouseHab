# Generated by Django 5.1 on 2024-09-02 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatemaster', '0064_rename_ceilingheights_rentcommercialadvertisement_ceilingheight_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='deposit',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Залог'),
        ),
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='deposit_currency',
            field=models.CharField(blank=True, choices=[('MZN', 'MZN'), ('USD', 'USD'), ('EUR', 'EUR')], default='MZN', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rentlongadvertisement',
            name='currency',
            field=models.CharField(choices=[('MZN', 'MZN'), ('USD', 'USD'), ('EUR', 'EUR')], default='MZN', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rentlongadvertisement',
            name='prepaymentPeriod',
            field=models.CharField(blank=True, choices=[('1_month', 'За 1 месяц'), ('2_months', '2 месяца'), ('3_months', '3 месяца'), ('4+_months', '4+')], max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='rentlongadvertisement',
            name='rentalTerm',
            field=models.CharField(choices=[('several_months', 'Несколько месяцев'), ('year', 'От года')], max_length=70),
        ),
        migrations.AlterField(
            model_name='salecommercialadvertisement',
            name='phone',
            field=models.CharField(blank=True, max_length=30, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='salecommercialadvertisement',
            name='price_per_m2',
            field=models.PositiveIntegerField(blank=True, verbose_name='Цена за м2'),
        ),
        migrations.AlterField(
            model_name='salecommercialadvertisement',
            name='tax',
            field=models.CharField(blank=True, choices=[('VAT_included', 'Ндс включен'), ('tax_exempt', 'Ндс не облагается'), ('simplified_tax', 'Упрощенная налогообложения')], max_length=50),
        ),
        migrations.AlterField(
            model_name='salecommercialadvertisement',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, verbose_name='Цена за всё'),
        ),
        migrations.AlterField(
            model_name='saleresidential',
            name='phone',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='saleresidential',
            name='saleType',
            field=models.CharField(blank=True, choices=[('onlySale', 'Только продаю'), ('buyingAnother', 'Одновременно покупаю другую')], max_length=50, null=True),
        ),
    ]