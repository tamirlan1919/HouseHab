# Generated by Django 5.0.6 on 2024-06-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatemaster', '0005_remove_professionalprofile_working_hours_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='professionalprofile',
            old_name='name_company',
            new_name='about_company',
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='bd',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='count_zhk',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='date_company',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='how_houses',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='how_houses_building',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='professionalprofile',
            name='role',
            field=models.CharField(choices=[('realtor', 'Риелтор'), ('agency', 'Агентство'), ('developer', 'Застройщик')], max_length=10),
        ),
    ]