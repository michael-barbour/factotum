# Generated by Django 2.2.1 on 2019-05-06 19:17

from django.db import migrations


def whitespace(fld):
    if fld:
        return fld.startswith(" ") or fld.endswith(" ")
    else:
        return False


def strip_whitespace(apps, schema_editor):
    """
    strip leading/trailing whitespace in "raw_chame_name" and "raw_cas" fields.
    """
    RawChem = apps.get_model("dashboard", "RawChem")

    for rc in RawChem.objects.all():
        if whitespace(rc.raw_chem_name):
            rc.raw_chem_name = rc.raw_chem_name.strip()
        if whitespace(rc.raw_cas):
            rc.raw_cas = rc.raw_cas.strip()
        rc.save()


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0108_rm_old_chem_fields")]

    operations = [
        migrations.RunPython(strip_whitespace, reverse_code=migrations.RunPython.noop)
    ]
