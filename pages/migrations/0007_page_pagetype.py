# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-15 04:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_block_blocktype'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='pagetype',
            field=models.CharField(default='Regular', max_length=50),
        ),
    ]
