# Generated by Django 2.1.2 on 2018-10-31 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0070_auto_20181026_0245")]

    operations = [
        migrations.AddField(
            model_name="documenttype",
            name="code",
            field=models.CharField(blank=True, default="??", max_length=2),
        )
    ]
