# Generated by Django 2.0.7 on 2018-09-14 12:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0064_remove_datadocument_uploaded_at")]

    operations = [
        migrations.AddField(
            model_name="datagroup",
            name="fs_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        )
    ]
