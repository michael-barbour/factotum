# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0005_datagroup_downloaded_by")]

    operations = [
        migrations.AlterField(
            model_name="datagroup",
            name="extraction_script",
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="datagroup",
            name="updated_at",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
    ]
