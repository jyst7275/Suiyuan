# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 09:53
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cellphone', models.CharField(max_length=20, unique=True)),
                ('username', models.CharField(default='nobody', max_length=20)),
                ('email', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('province', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('detail', models.CharField(max_length=50)),
                ('cellphone', models.CharField(max_length=20)),
                ('data_index', models.SlugField(max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flownews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Hotproduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 17, 53, 22, 654677))),
                ('order_address', models.CharField(max_length=100)),
                ('order_total', models.FloatField()),
                ('order_username', models.CharField(max_length=10)),
                ('order_index', models.SlugField(max_length=20, null=True)),
                ('order_cellphone', models.CharField(max_length=20)),
                ('order_status', models.CharField(max_length=20)),
                ('order_buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_count', models.IntegerField()),
                ('order_price', models.FloatField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiyuan.Order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_date', models.DateTimeField()),
                ('pay_method', models.CharField(max_length=200)),
                ('pay_data', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Passage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 53, 22, 648515, tzinfo=utc), verbose_name='date published')),
                ('pass_type', models.CharField(choices=[('News', '公司新闻'), ('Business', '行业动态'), ('Health', '健康知识')], max_length=20)),
                ('pass_title', models.CharField(max_length=100)),
                ('pass_summery', models.CharField(max_length=500)),
                ('pass_img', models.ImageField(null=True, upload_to='uploads/%Y/%m/%d/')),
                ('pass_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_index', models.SlugField(max_length=100, null=True)),
                ('product_img', models.ImageField(upload_to='uploads/product/')),
                ('product_summery', models.CharField(max_length=200)),
                ('product_description', models.TextField()),
                ('product_prize', models.FloatField()),
                ('product_date', models.DateField(default=datetime.date(2012, 1, 1), verbose_name='Up_to_Market')),
                ('img_1', models.ImageField(blank=True, null=True, upload_to='uploads/product/')),
                ('img_2', models.ImageField(blank=True, null=True, upload_to='uploads/product/')),
                ('img_3', models.ImageField(blank=True, null=True, upload_to='uploads/product/')),
                ('img_4', models.ImageField(blank=True, null=True, upload_to='uploads/product/')),
                ('img_5', models.ImageField(blank=True, null=True, upload_to='uploads/product/')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('is_subclass', models.BooleanField()),
                ('img', models.ImageField(upload_to='uploads/productCategory/')),
                ('count', models.IntegerField()),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='suiyuan.ProductCategory')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiyuan.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Topnews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summery', models.CharField(max_length=500)),
                ('set_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Latest')),
                ('passage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiyuan.Passage')),
            ],
        ),
        migrations.CreateModel(
            name='UserCode',
            fields=[
                ('usercode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=6)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiyuan.ProductCategory'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiyuan.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_pay',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='suiyuan.OrderPay'),
        ),
        migrations.AddField(
            model_name='hotproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiyuan.Product'),
        ),
        migrations.AddField(
            model_name='flownews',
            name='passage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiyuan.Passage'),
        ),
    ]
