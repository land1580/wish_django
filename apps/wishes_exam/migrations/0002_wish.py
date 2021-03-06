# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-25 17:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wishes_exam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('granted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='wishes_exam.User')),
                ('likes', models.ManyToManyField(related_name='liked', to='wishes_exam.User')),
            ],
        ),
    ]
