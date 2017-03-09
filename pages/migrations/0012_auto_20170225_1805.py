# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 23:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20170216_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckboxBlock',
            fields=[
                ('block_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.Block')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.block',),
        ),
        migrations.CreateModel(
            name='CheckboxItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.BooleanField(default=False)),
                ('placement', models.PositiveSmallIntegerField(blank=True)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkboxes', to='pages.CheckboxBlock')),
            ],
            options={
                'ordering': ('placement',),
            },
        ),
        migrations.AddField(
            model_name='block',
            name='help_text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='blocktype',
            field=models.CharField(blank=True, choices=[('T', 'Text'), ('A', 'Accordion'), ('C', 'Contact'), ('I', 'Info'), ('H', 'H')], max_length=50),
        ),
        migrations.AlterField(
            model_name='statepage',
            name='state',
            field=models.CharField(choices=[('AL', 'ALABAMA'), ('AK', 'ALASKA'), ('AZ', 'ARIZONA'), ('AR', 'ARKANSAS'), ('CA', 'CALIFORNIA'), ('CO', 'COLORADO'), ('CT', 'CONNECTICUT'), ('DE', 'DELAWARE'), ('FL', 'FLORIDA'), ('GA', 'GEORGIA'), ('HI', 'HAWAII'), ('ID', 'IDAHO'), ('IL', 'ILLINOIS'), ('IN', 'INDIANA'), ('IA', 'IOWA'), ('KS', 'KANSAS'), ('KY', 'KENTUCKY'), ('LA', 'LOUISIANA'), ('ME', 'MAINE'), ('MD', 'MARYLAND'), ('MA', 'MASSACHUSETTS'), ('MI', 'MICHIGAN'), ('MN', 'MINNESOTA'), ('MS', 'MISSISSIPPI'), ('MO', 'MISSOURI'), ('MT', 'MONTANA'), ('NE', 'NEBRASKA'), ('NV', 'NEVADA'), ('NH', 'HAMPSHIRE'), ('NJ', 'NEW JERSEY'), ('NM', 'NEW MEXICO'), ('NY', 'NEW YORK'), ('NC', 'NORTH CAROLINA'), ('ND', 'NORTH DAKOTA'), ('OH', 'OHIO'), ('OK', 'OKLAHOMA'), ('OR', 'OREGON'), ('PA', 'PENNSYLVANIA'), ('RI', 'RHODE ISLAND'), ('SC', 'CAROLINA'), ('SD', 'DAKOTA'), ('TN', 'TENNESSEE'), ('TX', 'TEXAS'), ('UT', 'UTAH'), ('VT', 'VERMONT'), ('VA', 'VIRGINIA'), ('WA', 'WASHINGTON'), ('WV', 'WEST VIRGINIA'), ('WI', 'WISCONSIN'), ('WY', 'WYOMING')], max_length=1, unique=True),
        ),
    ]
