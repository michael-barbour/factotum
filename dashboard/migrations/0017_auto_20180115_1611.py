# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-15 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0016_remove_productdocument_upc")]

    operations = [
        migrations.AddField(
            model_name="product",
            name="model_number",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="large_image",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="medium_image",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="thumb_image",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="product", name="title", field=models.CharField(max_length=255)
        ),
        migrations.AlterField(
            model_name="product",
            name="upc",
            field=models.CharField(db_index=True, max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="url",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
