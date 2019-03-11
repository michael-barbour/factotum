# Generated by Django 2.1.2 on 2019-03-11 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0094_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractedlistpresence',
            name='qa_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='qagroup',
            name='extracted_cpcat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.ExtractedCPCat'),
        ),
        migrations.AlterField(
            model_name='qagroup',
            name='extraction_script',
            field=models.ForeignKey(blank=True, limit_choices_to={'script_type': 'EX'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Script'),
        ),
    ]
