# Generated by Django 2.0.7 on 2018-07-27 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0058_auto_20180720_1434")]

    operations = [
        migrations.RemoveField(model_name="extractedtext", name="record_type")
    ]
