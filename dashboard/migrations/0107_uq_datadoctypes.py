# Generated by Django 2.2 on 2019-04-29 11:38
import django
from django.db import migrations, models
import django.db.models.deletion


def consolidate_null_unidentified(apps, schema_editor):
    """Updates DataDocument records with a DocumentType of "Unidentified" to be NULL.
  Removes "Unidentified" DocumentTypes."""
    DocumentType = apps.get_model("dashboard", "DocumentType")
    DataDocument = apps.get_model("dashboard", "DataDocument")
    qs_un_doctypes = DocumentType.objects.filter(title="Unidentified")
    (
        DataDocument.objects.filter(document_type__in=qs_un_doctypes).update(
            document_type=None
        )
    )
    qs_un_doctypes.delete()


def fwd_load_compatibility(apps, schema_editor):
    """Fills DocumentTypeGroupTypeCompatibilty based on old non-uniqe DocumentType.group_type.
    If 2+ groups are associated with 2+ document types, but the document type titles are identical,
    only one document type is linked to.
    """
    DocumentType = apps.get_model("dashboard", "DocumentType")
    DocumentTypeGroupTypeCompatibilty = apps.get_model(
        "dashboard", "DocumentTypeGroupTypeCompatibilty"
    )
    document_type_id_dict = {}
    doctype_grouptype_arr = []
    for document_type in DocumentType.objects.all():
        if document_type.title not in document_type_id_dict:
            document_type_id_dict[document_type.title] = document_type.id
        doctype_grouptype_arr.append(
            DocumentTypeGroupTypeCompatibilty(
                document_type_id=document_type_id_dict[document_type.title],
                group_type_id=document_type.group_type_id,
            )
        )
    DocumentTypeGroupTypeCompatibilty.objects.bulk_create(doctype_grouptype_arr)


def rev_load_compatibility(apps, schema_editor):
    """Reverses fwd_load_compatibility(...)
    """
    DocumentTypeGroupTypeCompatibilty.objects.all().delete()


def update_datadoc_doctype(apps, schema_editor):
    """Updates DataDocument records that point to the older non-unique
    document type to point to the document type that we will now be using
    as the unique document type.
    """
    DataDocument = apps.get_model("dashboard", "DataDocument")
    DocumentType = apps.get_model("dashboard", "DocumentType")
    DocumentTypeGroupTypeCompatibilty = apps.get_model(
        "dashboard", "DocumentTypeGroupTypeCompatibilty"
    )
    qs_doctype_old = DocumentType.objects.exclude(
        id__in=(DocumentTypeGroupTypeCompatibilty.objects.values("document_type_id"))
    )
    qs_doctype_new = DocumentType.objects.filter(
        id__in=(DocumentTypeGroupTypeCompatibilty.objects.values("document_type_id"))
    )
    for doctype_old in qs_doctype_old:
        doctype_new = qs_doctype_new.filter(title=doctype_old.title).get()
        (
            DataDocument.objects.filter(document_type=doctype_old).update(
                document_type=doctype_new
            )
        )


def rm_nonunique_doctypes(apps, schema_editor):
    """Removes the older non-unique document types from the table"""
    DocumentType = apps.get_model("dashboard", "DocumentType")
    DocumentTypeGroupTypeCompatibilty = apps.get_model(
        "dashboard", "DocumentTypeGroupTypeCompatibilty"
    )
    (
        DocumentType.objects.exclude(
            id__in=(
                DocumentTypeGroupTypeCompatibilty.objects.values("document_type_id")
            )
        ).delete()
    )


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0106_uq_datadoctypes")]

    operations = [
        migrations.RunPython(consolidate_null_unidentified),
        migrations.RunPython(fwd_load_compatibility, rev_load_compatibility),
        migrations.RunPython(update_datadoc_doctype),
        migrations.RunPython(rm_nonunique_doctypes),
        migrations.RemoveField(model_name="documenttype", name="group_type"),
        migrations.AlterField(
            model_name="documenttype",
            name="code",
            field=models.CharField(blank=True, default="??", max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name="documenttype",
            name="title",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name="documenttype",
            name="group_types",
            field=models.ManyToManyField(
                related_name="groups",
                through="dashboard.DocumentTypeGroupTypeCompatibilty",
                to="dashboard.GroupType",
            ),
        ),
    ]
