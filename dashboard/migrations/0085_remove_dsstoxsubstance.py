# Generated by Django 2.1.2 on 2019-02-05 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0084_move_sid_to_rawchem")]

    operations = [
        migrations.RemoveField(model_name="dsstoxsubstance", name="rawchem_ptr"),
        migrations.DeleteModel(name="DSSToxSubstance"),
    ]
