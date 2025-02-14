# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-31 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0044_auto_20180518_1416")]

    operations = [
        migrations.CreateModel(
            name="ProductAttribute",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("title", models.CharField(max_length=75)),
                ("type", models.CharField(max_length=75)),
            ],
            options={"ordering": ("title",)},
        ),
        migrations.CreateModel(
            name="ProductToAttribute",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.Product",
                    ),
                ),
                (
                    "product_attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.ProductAttribute",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddField(
            model_name="productattribute",
            name="products",
            field=models.ManyToManyField(
                through="dashboard.ProductToAttribute", to="dashboard.Product"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="attributes",
            field=models.ManyToManyField(
                through="dashboard.ProductToAttribute", to="dashboard.ProductAttribute"
            ),
        ),
    ]
