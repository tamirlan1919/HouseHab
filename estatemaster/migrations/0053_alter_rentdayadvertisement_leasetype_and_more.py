# Generated by Django 5.1 on 2024-08-25 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatemaster', '0052_remove_rentcommercialadvertisement_promotion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentdayadvertisement',
            name='leaseType',
            field=models.CharField(blank=True, choices=[('longTerm', 'Длительно'), ('daily', 'Посуточно')], max_length=70),
        ),
        migrations.AlterField(
            model_name='rentlongadvertisement',
            name='leaseType',
            field=models.CharField(blank=True, choices=[('longTerm', 'Длительно'), ('daily', 'Посуточно')], max_length=70),
        ),
        migrations.AlterField(
            model_name='salecommercialadvertisement',
            name='buildingName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]