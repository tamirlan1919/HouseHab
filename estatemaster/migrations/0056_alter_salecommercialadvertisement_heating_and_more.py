# Generated by Django 5.1 on 2024-08-26 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatemaster', '0055_alter_rentcommercialadvertisement_heating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salecommercialadvertisement',
            name='heating',
            field=models.CharField(blank=True, choices=[('autonomous', 'Автономное'), ('central', 'Центральное'), ('none', 'Нет')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='salecommercialadvertisement',
            name='сonditioning',
            field=models.CharField(blank=True, choices=[('local', 'Местное'), ('central', 'Центральное'), ('none', 'Нет')], max_length=30, null=True),
        ),
    ]