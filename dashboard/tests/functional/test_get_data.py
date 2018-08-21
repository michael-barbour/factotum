from django.urls import resolve
from django.test import TestCase, override_settings
from django.test.client import Client

from dashboard import views

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from dashboard.models import PUC, Product, ProductToPUC, ProductDocument
from dashboard.views.get_data import * 

@override_settings(ALLOWED_HOSTS=['testserver'])
class TestGetData(TestCase):
    fixtures = ['00_superuser.yaml', '01_lookups.yaml',
                '02_datasource.yaml', '03_datagroup.yaml', '04_PUC.yaml',
                '05_product.yaml', '06_datadocument.yaml','07_script.yaml',
                '08_extractedtext.yaml', '09_productdocument.yaml', '10_extractedchemical', '11_dsstoxsubstance']

    def setUp(self):
        self.client = Client()

    def test_dtxsid_stats(self):
        dtxs =["DTXSID9022528", "DTXSID1020273","DTXSID6026296","DTXSID2021781"]
        # Functional test: the stats calculation
        stats = stats_by_dtxsids(dtxs)
        print(stats)
        # select out the stats for one DTXSID, ethylparaben
        ethylparaben_stats = stats.get(sid='DTXSID9022528')
        self.assertEqual(0, ethylparaben_stats['pucs_n'])

        self.client.login(username='Karyn', password='specialP@55word')
        # get the associated documents for linking to products
        dds = DataDocument.objects.filter(pk__in=DSSToxSubstance.objects.filter(sid='DTXSID9022528').\
        values('extracted_chemical__extracted_text__data_document'))
        dd = dds[0]

        print(dd.__dict__)
        print('dd pk: %s' % dd.pk)
        print('dd document_type: %s' % dd.document_type)
        print('--related products before linking:')
        print(dd.products.all())
        ds = dd.data_group.data_source
        p = Product.objects.create(data_source=ds, title='Test Product',
                                upc='Test UPC for ProductToPUC')
        pd = ProductDocument.objects.create(document=dd, product=p)
        pd.save()
        dd.refresh_from_db()
        print('--related products after linking:')
        print(dd.products.all())
        # get one of the products that was just linked to a data document with DTXSID9022528 in its extracted chemicals
        pid = dd.products.first().pk
        puc = PUC.objects.get(id=20)
        # add a puc to one of the products containing ethylparaben

        ppuc = ProductToPUC.objects.create(product=Product.objects.get(pk=pid),
                                        PUC=puc,
                                        puc_assigned_usr=User.objects.get(username='karyn'))
        ppuc.refresh_from_db()
        print(p.producttopuc_set.__dict__)
        stats = stats_by_dtxsids(dtxs)
        print(stats)
        # select out the stats for one DTXSID, ethylparaben
        ethylparaben_stats = stats.get(sid='DTXSID9022528')
        self.assertEqual(1, ethylparaben_stats['pucs_n'])

        #csv_out = download_chem_stats(stats)
        #print(csv_out.content)




