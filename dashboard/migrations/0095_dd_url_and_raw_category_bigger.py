# Generated by Django 2.1.7 on 2019-03-07 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0094_unique_together")]

    operations = [
        migrations.AlterField(
            model_name="datadocument",
            name="raw_category",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="datadocument",
            name="url",
            field=models.CharField(blank=True, max_length=275, null=True),
        ),
    ]
