# Generated by Django 5.1 on 2024-09-02 12:13

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estatemaster', '0063_alter_saleresidential_apartmententrance_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentcommercialadvertisement',
            old_name='ceilingHeights',
            new_name='ceilingHeight',
        ),
        migrations.RenameField(
            model_name='salecommercialadvertisement',
            old_name='ceilingHeights',
            new_name='ceilingHeight',
        ),
        migrations.AlterField(
            model_name='rentlongadvertisement',
            name='apartmentEntrance',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('ramp', 'Пандус'), ('trashChute', 'Мусоропровод')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='rentlongadvertisement',
            name='viewFromWindow',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('outside', 'На улицу'), ('courtyard', 'Во двор'), ('atSea', 'На море')], max_length=23, null=True),
        ),
        migrations.AlterField(
            model_name='saleresidential',
            name='apartmentEntrance',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('ramp', 'Пандус'), ('trashChute', 'Мусоропровод')], max_length=15, null=True),
        ),
    ]