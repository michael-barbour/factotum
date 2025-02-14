# Generated by Django 2.1.2 on 2019-02-11 23:02

from django.db import migrations, models
import django.db.models.deletion


def set_extractedtext(apps, schema_editor):
    """
    Populate all the new keys
    """
    RawChem = apps.get_model("dashboard", "RawChem")
    for rawchem in RawChem.objects.all():
        id = rawchem.id
        # print(f'RawChem %s : %s' % (id, rawchem))
        try:
            et = (
                apps.get_model("dashboard.ExtractedChemical")
                .objects.get(rawchem_ptr=id)
                .extracted_text
            )
        except apps.get_model("dashboard.ExtractedChemical").DoesNotExist:
            try:
                et = (
                    apps.get_model("dashboard.ExtractedFunctionalUse")
                    .objects.get(rawchem_ptr=id)
                    .extracted_text
                )
            except apps.get_model("dashboard.ExtractedFunctionalUse").DoesNotExist:
                try:
                    et = (
                        apps.get_model("dashboard.ExtractedListPresence")
                        .objects.get(rawchem_ptr=id)
                        .extracted_cpcat
                    )
                except apps.get_model("dashboard.ExtractedListPresence").DoesNotExist:
                    et = None
        rawchem.extracted_text_new = et
        rawchem.save()


def remove_extractedtext(apps, schema_editor):
    """
    remove all the new keys
    """
    RawChem = apps.get_model("dashboard", "RawChem")
    for rawchem in RawChem.objects.all():
        rawchem.extracted_text_new = None
        rawchem.save()


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0087_auto_20190213_1733")]

    operations = [
        migrations.AddField(
            model_name="rawchem",
            name="extracted_text_new",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="extracted_chemical",
                to="dashboard.ExtractedText",
            ),
        ),
        migrations.RunPython(set_extractedtext, reverse_code=remove_extractedtext),
        migrations.RemoveField(model_name="extractedchemical", name="extracted_text"),
        migrations.RemoveField(
            model_name="extractedfunctionaluse", name="extracted_text"
        ),
        migrations.RemoveField(
            model_name="extractedlistpresence", name="extracted_cpcat"
        ),
        migrations.RenameField(
            model_name="rawchem",
            old_name="extracted_text_new",
            new_name="extracted_text",
        ),
        migrations.AlterField(
            model_name="rawchem",
            name="extracted_text",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rawchem",
                to="dashboard.ExtractedText",
            ),
        ),
    ]
