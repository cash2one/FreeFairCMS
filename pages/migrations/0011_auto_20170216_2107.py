# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 02:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_auto_20170216_1427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='infocategory',
            options={'ordering': ('placement',)},
        ),
        migrations.AlterModelOptions(
            name='infocontent',
            options={'ordering': ('placement',)},
        ),
        migrations.AddField(
            model_name='infocategory',
            name='placement',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='infocontent',
            name='placement',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]