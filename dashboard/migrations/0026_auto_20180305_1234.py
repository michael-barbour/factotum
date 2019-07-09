# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-05 12:34
from __future__ import unicode_literals

import dashboard.models.data_source
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0025_extractionscript_qa_begun")]

    operations = [
        migrations.CreateModel(
            name="Script",
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
                ("title", models.CharField(max_length=50)),
                (
                    "url",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                    ),
                ),
                ("qa_begun", models.BooleanField(default=False)),
                (
                    "script_type",
                    models.CharField(
                        choices=[
                            ("DL", "download"),
                            ("EX", "extraction"),
                            ("PC", "product categorization"),
                        ],
                        default="EX",
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(model_name="datadocument", name="data_source"),
        migrations.AddField(
            model_name="datadocument",
            name="uploaded_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="datagroup",
            name="download_script",
            field=models.ForeignKey(
                blank=True,
                default=1,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dashboard.Script",
            ),
        ),
        migrations.AlterField(
            model_name="datasource",
            name="estimated_records",
            field=models.PositiveIntegerField(
                default=47, validators=[dashboard.models.data_source.validate_nonzero]
            ),
        ),
        migrations.AlterField(
            model_name="extractedtext",
            name="extraction_script",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="dashboard.Script",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="brand_name",
            field=models.CharField(
                blank=True, db_index=True, default="", max_length=200, null=True
            ),
        ),
        migrations.DeleteModel(name="ExtractionScript"),
    ]
