# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-19 18:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0019_auto_20180118_0745")]

    operations = [
        migrations.CreateModel(
            name="ExtractedChemical",
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
                ("cas", models.CharField(blank=True, max_length=200, null=True)),
                ("chem_name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "raw_min_comp",
                    models.DecimalField(
                        blank=True, decimal_places=15, max_digits=20, null=True
                    ),
                ),
                (
                    "raw_max_comp",
                    models.DecimalField(blank=True, decimal_places=15, max_digits=20),
                ),
                (
                    "point_composition",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=2, null=True
                    ),
                ),
                (
                    "units",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("percent composition", "percent composition"),
                            ("weight fraction", "weight fraction"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "reported_functional_use",
                    models.CharField(blank=True, max_length=100),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExtractedText",
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
                ("doc_date", models.DateField(blank=True)),
                ("rev_num", models.PositiveIntegerField(blank=True)),
                (
                    "data_document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.DataDocument",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="extractedchemical",
            name="extracted_text",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="dashboard.ExtractedText",
            ),
        ),
    ]
