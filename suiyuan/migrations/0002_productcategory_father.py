# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-02 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suiyuan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='father',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='suiyuan.ProductCategory'),
        ),
    ]
