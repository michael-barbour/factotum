# Generated by Django 2.0.7 on 2018-09-06 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0063_auto_20180906_2017")]

    operations = [migrations.RemoveField(model_name="datadocument", name="uploaded_at")]
