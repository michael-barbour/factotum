# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-08 09:28
from __future__ import unicode_literals

from django.db import migrations
from dashboard.models.group_type import GroupType
from dashboard.models.document_type import DocumentType


def create_default_data_group_type(apps, schema_editor):
    # create the default "unidentified" group_type
    GroupType.objects.create(title='Unidentified', description='Unidentified Group Type')

    data_group = apps.get_model('dashboard', 'DataGroup')
    for dg in data_group.objects.all():
        dg.group_type_id = 1
        dg.save()


def create_default_document_type(apps, schema_editor):
    # create the default "unidentified" document_type
    DocumentType.objects.create(title='Unidentified', description='Unidentified Document Type', group_type_id=1)

    docs = apps.get_model('dashboard', 'DataDocument')
    for dd in docs.objects.all():
        dd.document_type_id = 1
        dd.save()


class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0048_datagroup_group_type'),
    ]

    # operations = [
    #     migrations.RunPython(create_default_data_group_type),
    #     migrations.RunPython(create_default_document_type),
    # ]
