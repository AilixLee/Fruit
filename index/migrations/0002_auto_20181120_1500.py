# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-20 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uphone', models.CharField(max_length=11, verbose_name='手机号')),
                ('upwd', models.CharField(max_length=30, verbose_name='密码')),
                ('uemail', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('uname', models.CharField(max_length=30, verbose_name='用户名')),
                ('isActive', models.BooleanField(default=True, verbose_name='用户状态')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'users',
            },
        ),
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '商品', 'verbose_name_plural': '商品'},
        ),
    ]