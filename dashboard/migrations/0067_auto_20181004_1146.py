# Generated by Django 2.0.8 on 2018-10-04 11:46

import dashboard.models.data_group
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0066_auto_20181004_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puc',
            name='attribute',
        ),
        migrations.DeleteModel(
            name='PUCAttribute',
        ),
    ]
