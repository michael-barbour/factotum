# drop and replace schema local_factotum

# the yaml version of the production database is only compatible with 
# a modified version of migration 30. I removed the DSSToxSubstance model
# addition because it's already in there

# python manage.py loaddata prod_20180328

from django.contrib.auth.models import User
from dashboard.models import DataSource, DataGroup, DataDocument, ProductDocument, Product, ProductCategory
from django.db.models import Count


Product.objects.count()
DataDocument.objects.count()
ProductCategory.objects.count()
# Objects related to User:
DataGroup.objects.values('downloaded_by__username').annotate(n=Count('id'))
Product.objects.values('puc_assigned_usr_id__username').annotate(n=Count('id'))
# before: 
# <QuerySet [{'puc_assigned_usr_id': None, 'assigned': 463}, 
#            {'puc_assigned_usr_id': 1, 'assigned': 1}, 
#            {'puc_assigned_usr_id': 3, 'assigned': 1}]>
# after deleting user 3:
# <QuerySet [{'puc_assigned_usr_id': None, 'assigned': 463}, 
#            {'puc_assigned_usr_id': 1, 'assigned': 1}]>

ProductCategory.objects.values('last_edited_by').annotate(n=Count('id'))


# <QuerySet [{'puc_assigned_usr_id': None, 'assigned': 463}, 
#    {'puc_assigned_usr_id': 1, 'assigned': 1}, {'puc_assigned_usr_id': 3, 'assigned': 1}]>
User.objects.filter(id=3).delete()


User.objects.filter(id__gt=1).delete()


python manage.py dumpdata dashboard.sourcetype --format=yaml > ./dashboard/fixtures/01_sourcetype.yaml
python manage.py dumpdata dashboard.datasource --format=yaml > ./dashboard/fixtures/02_datasource.yaml
python manage.py dumpdata dashboard.datagroup --format=yaml > ./dashboard/fixtures/03_datagroup.yaml
python manage.py dumpdata dashboard.productcategory --format=yaml > ./dashboard/fixtures/04_productcategory.yaml
python manage.py dumpdata dashboard.product --format=yaml > ./dashboard/fixtures/05_product.yaml
python manage.py dumpdata dashboard.datadocument --format=yaml > ./dashboard/fixtures/06_datadocument.yaml
python manage.py dumpdata dashboard.script --format=yaml > ./dashboard/fixtures/07_script.yaml
python manage.py dumpdata dashboard.extractedtext --format=yaml > ./dashboard/fixtures/08_extractedtext.yaml
python manage.py dumpdata dashboard.productdocument --format=yaml > ./dashboard/fixtures/09_productdocument.yaml

