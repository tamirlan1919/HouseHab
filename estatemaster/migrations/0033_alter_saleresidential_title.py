# Generated by Django 5.1 on 2024-08-19 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatemaster', '0032_alter_saleresidential_housetype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleresidential',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]