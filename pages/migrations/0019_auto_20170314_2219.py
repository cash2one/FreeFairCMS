# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 02:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_auto_20170314_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagerevision',
            name='page',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='revision', to='pages.Page'),
        ),
    ]
