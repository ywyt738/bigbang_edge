# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20171113_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='senthistory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
