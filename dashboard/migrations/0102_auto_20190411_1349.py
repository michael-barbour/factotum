# Generated by Django 2.1.7 on 2019-04-11 13:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("dashboard", "0101_verbose_dsstox_names")]

    operations = [
        migrations.AlterField(
            model_name="script",
            name="url",
            field=models.CharField(
                blank=True,
                max_length=225,
                null=True,
                validators=[django.core.validators.URLValidator()],
            ),
        )
    ]
