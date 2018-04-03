# drop and replace schema local_factotum

# the yaml version of the production database is only compatible with 
# a modified version of migration 30. I removed the DSSToxSubstance model
# addition because it's already in there

# python manage.py loaddata prod_20180328
# python manage.py loaddata 00_superuser

from django.contrib.auth.models import User
from dashboard.models import DataSource, DataGroup, DataDocument, ProductDocument, Product, ProductCategory
from django.db.models import Count

# prep the objects by switching their related user to Karyn
karyn = User.objects.get(username='Karyn')

DataGroup.objects.values('downloaded_by__username').annotate(n=Count('id'))
Product.objects.values('puc_assigned_usr_id__username').annotate(n=Count('id'))

DataGroup.objects.all().update(downloaded_by=karyn)
Product.objects.all().update(puc_assigned_usr_id=karyn)

ProductCategory.objects.all().update(last_edited_by=karyn)

# Remove all the real-world users
User.objects.exclude(username='Karyn').delete()

ProductDocument.objects.filter(id=196)
ProductDocument.objects.get(id=196).product #192
ProductDocument.objects.get(id=196).document.id #1105

# delete products and datadocuments where their crosswalk id is greater than 200
ProductDocument.objects.filter(id__gt=200).select_related('document').delete()

# Delete the now-unlinked products
Product.objects.exclude(id__in=ProductDocument.objects.all().values('product_id')).delete()

# Delete a few more data groups
DataGroup.objects.filter(id__in=[19,23,24]).delete()




python manage.py dumpdata dashboard.sourcetype --format=yaml > ./dashboard/fixtures/01_sourcetype.yaml
python manage.py dumpdata dashboard.datasource --format=yaml > ./dashboard/fixtures/02_datasource.yaml
python manage.py dumpdata dashboard.datagroup --format=yaml > ./dashboard/fixtures/03_datagroup.yaml
python manage.py dumpdata dashboard.productcategory --format=yaml > ./dashboard/fixtures/04_productcategory.yaml
python manage.py dumpdata dashboard.product --format=yaml > ./dashboard/fixtures/05_product.yaml
python manage.py dumpdata dashboard.datadocument --format=yaml > ./dashboard/fixtures/06_datadocument.yaml
python manage.py dumpdata dashboard.script --format=yaml > ./dashboard/fixtures/07_script.yaml
python manage.py dumpdata dashboard.extractedtext --format=yaml > ./dashboard/fixtures/08_extractedtext.yaml
python manage.py dumpdata dashboard.productdocument --format=yaml > ./dashboard/fixtures/09_productdocument.yaml

