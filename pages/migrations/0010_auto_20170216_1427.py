# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20170212_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infocontent',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='infocontent',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='infocontent',
            name='groups',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='infocontent',
            name='reading',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='infocontent',
            name='templates',
            field=models.TextField(blank=True),
        ),
    ]