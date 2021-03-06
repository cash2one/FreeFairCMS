# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_auto_20170225_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='blocktype',
            field=models.CharField(blank=True, choices=[('T', 'Text'), ('A', 'Accordion'), ('C', 'Contact'), ('I', 'Info'), ('H', 'Checkbox')], max_length=50),
        ),
        migrations.AlterField(
            model_name='textblock',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
