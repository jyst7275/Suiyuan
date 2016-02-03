# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-02 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suiyuan', '0002_productcategory_father'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_price',
            new_name='product_prize',
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='suiyuan.ProductCategory'),
        ),
    ]
