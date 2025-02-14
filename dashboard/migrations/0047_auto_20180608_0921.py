# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-08 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0046_auto_20180604_0828")]

    operations = [
        migrations.CreateModel(
            name="DocumentType",
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
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={"ordering": ("title",)},
        ),
        migrations.CreateModel(
            name="GroupType",
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
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={"ordering": ("title",)},
        ),
        migrations.RemoveField(model_name="datadocument", name="source_type"),
        migrations.RemoveField(model_name="datasource", name="type"),
        migrations.DeleteModel(name="SourceType"),
        migrations.AddField(
            model_name="documenttype",
            name="group_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="group",
                to="dashboard.GroupType",
            ),
        ),
        migrations.AddField(
            model_name="datadocument",
            name="document_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="dashboard.DocumentType",
            ),
        ),
    ]
