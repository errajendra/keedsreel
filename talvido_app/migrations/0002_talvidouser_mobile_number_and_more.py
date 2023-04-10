# Generated by Django 4.2 on 2023-04-10 05:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talvido_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='talvidouser',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Mobile Number'),
        ),
        migrations.AlterField(
            model_name='talvidouser',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Full Name'),
        ),
    ]
