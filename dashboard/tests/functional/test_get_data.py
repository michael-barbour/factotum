from django.urls import resolve
from django.test import TestCase, override_settings
from django.test.client import Client

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from dashboard.models import PUC, Product, ProductToPUC, ProductDocument, DSSToxLookup
from dashboard.views.get_data import *
from django.test import TestCase
from django.test.client import Client

from dashboard.views.get_data import *
from dashboard.tests.loader import fixtures_standard


# from dashboard import views
# from django.urls import resolve
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User

@override_settings(ALLOWED_HOSTS=['testserver'])
class TestGetData(TestCase):

    fixtures = fixtures_standard

    def setUp(self):
        self.client = Client()

    def test_dtxsid_pucs_n(self):
        dtxs = ["DTXSID9022528", "DTXSID1020273",
                "DTXSID6026296", "DTXSID2021781"]
        # Functional test: the stats calculation
        stats = stats_by_dtxsids(dtxs)
        # select out the stats for one DTXSID, ethylparaben
        ethylparaben_stats = stats.get(sid='DTXSID9022528')
        dsstox = DSSToxLookup.objects.get(sid='DTXSID9022528')
        self.assertEqual(dsstox.puc_count, ethylparaben_stats['pucs_n'], 
                        (f'There should be {dsstox.puc_count}) '
                        'PUC associated with ethylparaben'))

        self.client.login(username='Karyn', password='specialP@55word')
        # get the associated documents for linking to products
        dds = DataDocument.objects.filter(pk__in=ExtractedChemical.objects.filter(dsstox__sid='DTXSID9022528').
                                          values('extracted_text__data_document'))
        dd = dds[0]

        ds = dd.data_group.data_source
        p = Product.objects.create(data_source=ds, title='Test Product',
                                   upc='Test UPC for ProductToPUC')
        pd = ProductDocument.objects.create(document=dd, product=p)
        dd.refresh_from_db()

        # get one of the products that was just linked to a data document with DTXSID9022528 in its extracted chemicals
        pid = dd.products.first().pk
        puc = PUC.objects.get(id=20)
        # add a puc to one of the products containing ethylparaben

        ppuc = ProductToPUC.objects.create(product=Product.objects.get(pk=pid),
                                           puc=puc,
                                           puc_assigned_usr=User.objects.get(username='Karyn'))
        ppuc.refresh_from_db()
        stats = stats_by_dtxsids(dtxs)
        # select out the stats for one DTXSID, ethylparaben
        ethylparaben_stats = stats.get(sid='DTXSID9022528')
        self.assertEqual(dsstox.puc_count, ethylparaben_stats['pucs_n'])

    def test_dtxsid_dds_n(self):
        dtxs = ["DTXSID9022528", "DTXSID1020273",
                "DTXSID6026296", "DTXSID2021781"]
        # Functional test: the stats calculation
        stats = stats_by_dtxsids(dtxs)
        for e in stats:
            if e['sid'] == 'DTXSID9022528':
                ethylparaben_stats = e

        self.assertEqual(
            2, ethylparaben_stats['dds_n'], 'There should be 2 datadocuments associated with ethylaraben')
        # change the number of related data documents by deleting one
        self.client.login(username='Karyn', password='specialP@55word')
        # get the associated documents for linking to products
        dds = DataDocument.objects.filter(pk__in=ExtractedChemical.objects.filter(dsstox__sid='DTXSID9022528').
                                          values('extracted_text__data_document'))

        dd = dds[0]
        dd.delete()

        stats = stats_by_dtxsids(dtxs)
        for e in stats:
            if e['sid'] == 'DTXSID9022528':
                ethylparaben_stats = e

        self.assertEqual(
            1, ethylparaben_stats['dds_n'], 'There should now be 1 datadocument associated with ethylaraben')

    def test_dtxsid_dds_wf_n(self):
        dtxs = ["DTXSID9022528", "DTXSID1020273",
                "DTXSID6026296", "DTXSID2021781"]
        # Functional test: the stats calculation
        stats = stats_by_dtxsids(dtxs)
        for e in stats:
            if e['sid'] == 'DTXSID9022528':
                ethylparaben_stats = e
        self.assertEqual(1, ethylparaben_stats['dds_wf_n'], 'There should be 1 extracted chemical \
        with weight fraction data associated with ethylparaben')
        # add weight fraction data to a different extractedchemical
        ec = ExtractedChemical.objects.get(rawchem_ptr_id=73)
        ec.raw_min_comp = 0.1
        ec.save()
        stats = stats_by_dtxsids(dtxs)
        for e in stats:
            if e['sid'] == 'DTXSID9022528':
                ethylparaben_stats = e

        self.assertEqual(2, ethylparaben_stats['dds_wf_n'], 'There should be 2 extracted chemicals \
        with weight fraction data associated with ethylparaben')

    def test_dtxsid_products_n(self):
        dtxs = ["DTXSID9022528", "DTXSID1020273",
                "DTXSID6026296", "DTXSID2021781"]
        # Functional test: the stats calculation
        stats = stats_by_dtxsids(dtxs)

        for e in stats:
            if e['sid'] == 'DTXSID9022528':
                ethylparaben_stats = e

        self.assertEqual(4, ethylparaben_stats['products_n'], 'There should be 4 products \
        associated with ethylparaben')
        self.client.login(username='Karyn', password='specialP@55word')
        # get the associated documents for linking to products
        dds = DataDocument.objects.filter(pk__in=ExtractedChemical.objects.filter(dsstox__sid='DTXSID9022528').
                                          values('extracted_text__data_document'))
        dd = dds[0]

        ds = dd.data_group.data_source
        p = Product.objects.create(data_source=ds, title='Test Product',
                                   upc='Test UPC for ProductToPUC')
        pd = ProductDocument.objects.create(document=dd, product=p)
        pd.save()
        dd.refresh_from_db()

        stats = stats_by_dtxsids(dtxs)
        for e in stats:
            if e['sid'] == 'DTXSID9022528':
                ethylparaben_stats = e
        self.assertEqual(5, ethylparaben_stats['products_n'], 'There should now be 5 products \
        associated with ethylparaben')

    def test_habits_and_practices_cards(self):
        data = {'puc': ['2']}
        response = self.client.post('/get_data/', data=data)
        for hnp in [b'ball bearings',
                    b'motorcycle',
                    b'vitamin a&amp;d',
                    b'dish soap']:
            self.assertIn(hnp, response.content)

    def test_download_pucs_button(self):
        response = self.client.get('/get_data/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Download PUCs')
        self.assertContains(response, 'Download PUC Attributes')

    def test_download_list_presence_keywords(self):
        response = self.client.get('/dl_lpkeywords/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'abrasive')
        self.assertContains(response, 'Velit neque aliquam etincidunt.')
