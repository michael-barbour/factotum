# Generated by Django 2.1.2 on 2018-12-28 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0081_refine_models")]

    operations = [
        migrations.RenameField(
            model_name="dsstoxsubstance",
            old_name="rawchem_ptr_temp",
            new_name="rawchem_ptr",
        ),
        migrations.RenameField(
            model_name="extractedchemical",
            old_name="rawchem_ptr_temp",
            new_name="rawchem_ptr",
        ),
        migrations.RenameField(
            model_name="extractedfunctionaluse",
            old_name="rawchem_ptr_temp",
            new_name="rawchem_ptr",
        ),
        migrations.RenameField(
            model_name="extractedlistpresence",
            old_name="rawchem_ptr_temp",
            new_name="rawchem_ptr",
        ),
        migrations.RenameField(
            model_name="ingredient", old_name="rawchem_ptr_temp", new_name="rawchem_ptr"
        ),
    ]
