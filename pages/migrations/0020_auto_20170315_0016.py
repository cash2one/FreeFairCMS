# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 04:16
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_auto_20170314_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagerevision',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]