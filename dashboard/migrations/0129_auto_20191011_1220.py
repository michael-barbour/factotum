# Generated by Django 2.2.1 on 2019-10-11 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("dashboard", "0128_remove_nulls_doc_group_type")]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="brand_name",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                help_text="brand name",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="color",
            field=models.CharField(
                blank=True, help_text="color", max_length=100, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="documents",
            field=models.ManyToManyField(
                help_text="Data Documents related to this Product",
                through="dashboard.ProductDocument",
                to="dashboard.DataDocument",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="item_id",
            field=models.IntegerField(blank=True, help_text="item ID", null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="large_image",
            field=models.CharField(
                blank=True, help_text="large image", max_length=500, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="long_description",
            field=models.TextField(blank=True, help_text="long description", null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="manufacturer",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                help_text="title",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="medium_image",
            field=models.CharField(
                blank=True, help_text="medium image", max_length=500, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="model_number",
            field=models.CharField(
                blank=True, help_text="model number", max_length=200, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="parent_item_id",
            field=models.IntegerField(
                blank=True, help_text="parent item ID", null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="short_description",
            field=models.TextField(
                blank=True, help_text="short description", null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="size",
            field=models.CharField(
                blank=True, help_text="size", max_length=100, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="source_category",
            field=models.ForeignKey(
                blank=True,
                help_text="The category assigned in the product's data source",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dashboard.SourceCategory",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="thumb_image",
            field=models.CharField(
                blank=True, help_text="thumbnail image", max_length=500, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="upc",
            field=models.CharField(
                db_index=True, help_text="UPC", max_length=60, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="url",
            field=models.CharField(
                blank=True, help_text="URL", max_length=500, null=True
            ),
        ),
        migrations.AlterField(
            model_name="puc",
            name="description",
            field=models.TextField(help_text="PUC description"),
        ),
        migrations.AlterField(
            model_name="puc",
            name="extracted_habits_and_practices",
            field=models.ManyToManyField(
                help_text="extracted Habits and Practices records assigned to this PUC",
                through="dashboard.ExtractedHabitsAndPracticesToPUC",
                to="dashboard.ExtractedHabitsAndPractices",
            ),
        ),
        migrations.AlterField(
            model_name="puc",
            name="gen_cat",
            field=models.CharField(help_text="general category", max_length=50),
        ),
        migrations.AlterField(
            model_name="puc",
            name="kind",
            field=models.CharField(
                blank=True,
                choices=[
                    ("UN", "unknown"),
                    ("FO", "formulations"),
                    ("AR", "articles"),
                    ("OC", "occupational"),
                ],
                default="UN",
                help_text="kind",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="puc",
            name="last_edited_by",
            field=models.ForeignKey(
                default=1,
                help_text="last edited by",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="puc",
            name="prod_fam",
            field=models.CharField(
                blank=True, default="", help_text="product family", max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="puc",
            name="prod_type",
            field=models.CharField(
                blank=True, default="", help_text="product type", max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="puc",
            name="products",
            field=models.ManyToManyField(
                help_text="products assigned to this PUC",
                through="dashboard.ProductToPUC",
                to="dashboard.Product",
            ),
        ),
        migrations.AlterField(
            model_name="rawchem",
            name="raw_cas",
            field=models.CharField(
                blank=True,
                help_text="Raw CAS",
                max_length=100,
                null=True,
                verbose_name="Raw CAS",
            ),
        ),
        migrations.AlterField(
            model_name="rawchem",
            name="raw_chem_name",
            field=models.CharField(
                blank=True,
                help_text="Raw chemical name",
                max_length=1300,
                null=True,
                verbose_name="Raw chemical name",
            ),
        ),
        migrations.AlterField(
            model_name="rawchem",
            name="rid",
            field=models.CharField(
                blank=True, help_text="RID", max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="sourcecategory",
            name="data_source",
            field=models.ForeignKey(
                help_text="data source",
                on_delete=django.db.models.deletion.CASCADE,
                to="dashboard.DataSource",
            ),
        ),
        migrations.AlterField(
            model_name="sourcecategory",
            name="path",
            field=models.CharField(
                blank=True, help_text="path", max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="sourcecategory",
            name="source_id",
            field=models.CharField(
                blank=True, help_text="source ID", max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="sourcecategory",
            name="source_parent_id",
            field=models.CharField(
                blank=True, help_text="source parent ID", max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="sourcecategory",
            name="title",
            field=models.CharField(help_text="title", max_length=200),
        ),
    ]
