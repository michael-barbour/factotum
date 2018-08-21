from django.urls import resolve
from django.test import TestCase
from django.test.client import Client

from dashboard import views

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from dashboard.models import PUC, Product, ProductToPUC
from dashboard.views.get_data import * 

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
        # add a puc to one of the products containing ethylparaben
        ps = DSSToxSubstance.objects.filter(sid='DTXSID9022528').\
        values('extracted_chemical__extracted_text__data_document__products')
        print('----- ps')
        print(ps)
        # get one of the products that is already linked to a data document with DTXSID9022528 in its extracted chemicals
        p = ps.first()
        puc = PUC.objects.get(id=20)
        ppuc = ProductToPUC.objects.create(product=p,
                                        PUC=puc,
                                        puc_assigned_usr=User.objects.get(username='karyn'))
        stats = stats_by_dtxsids(dtxs)
        print(stats)
        # select out the stats for one DTXSID, ethylparaben
        ethylparaben_stats = stats.get(sid='DTXSID9022528')
        self.assertEqual(1, ethylparaben_stats['pucs_n'])

        #csv_out = download_chem_stats(stats)
        #print(csv_out.content)




