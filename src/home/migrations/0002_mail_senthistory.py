# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 02:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_date', models.DateField(verbose_name='发送日期')),
                ('sent_count', models.SmallIntegerField(default=0, verbose_name='发送次数')),
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Host_info', verbose_name='主机')),
            ],
        ),
        migrations.CreateModel(
            name='SentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_date', models.DateField(verbose_name='发送日期')),
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Host_info', verbose_name='主机')),
            ],
        ),
    ]
