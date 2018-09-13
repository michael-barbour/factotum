# Generated by Django 2.0.7 on 2018-09-06 20:17

from django.db import migrations

def update_created_at_field(apps, schema_editor):

    document = apps.get_model('dashboard', 'DataDocument')

    for doc in document.objects.all():
        if doc.uploaded_at and doc.created_at:
            if doc.uploaded_at < doc.created_at:
                doc.created_at = doc.uploaded_at
                doc.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0062_add_datagroup_url'),
    ]

    operations = [
        migrations.RunPython(update_created_at_field, reverse_code=migrations.RunPython.noop),
    ]
