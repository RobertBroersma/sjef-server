# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 13:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('usersettings', '0004_dri_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='dri',
            name='nutritional_value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.NutritionalValue'),
        ),
    ]
