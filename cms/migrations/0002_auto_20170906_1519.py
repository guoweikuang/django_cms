# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-06 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='article',
            name='update_time',
            field=models.DateField(auto_now=True, verbose_name='更新时间'),
        ),
    ]