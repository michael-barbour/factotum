# Generated by Django 2.1.2 on 2018-10-19 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0066_auto_20180927_0935")]

    operations = [
        migrations.RenameField(
            model_name="extractedlistpresence",
            old_name="extracted_text",
            new_name="extracted_cpcat",
        ),
        migrations.AddField(
            model_name="grouptype",
            name="code",
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="datadocument",
            name="filename",
            field=models.CharField(max_length=255),
        ),
    ]
