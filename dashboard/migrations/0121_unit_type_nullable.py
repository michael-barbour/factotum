# Generated by Django 2.2.1 on 2019-07-10 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("dashboard", "0120_raw_chem_field_length")]

    operations = [
        migrations.AlterField(
            model_name="extractedchemical",
            name="unit_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="dashboard.UnitType",
            ),
        )
    ]
