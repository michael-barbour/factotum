from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import resolve
from django.contrib.auth.models import User
from haystack.management.commands import update_index, clear_index
from haystack import connections
import time
from django.conf import settings
from dashboard.models import DSSToxSubstance



@override_settings(HAYSTACK_CONN='test_index')
class ChemSearchTest(TestCase):
    fixtures = ['00_superuser.yaml', '01_lookups.yaml',
                '02_datasource.yaml', '03_datagroup.yaml', '04_PUC.yaml',
                '05_product.yaml', '06_datadocument.yaml', '07_script.yaml',
                '08_extractedtext.yaml', '09_productdocument.yaml', '10_extractedchemical', '11_dsstoxsubstance']

    def setUp(self):
        print('Test case setUp() method running')
        self.c = Client()
        index_start = time.time()
        update_index.Command().handle( remove=True, using=['test_index'], interactive=False)
        index_elapsed = time.time() - index_start
        print('Indexing took %s seconds' % index_elapsed)

    def tearDown(self):
        clear_index.Command().handle( using=['test_index'], interactive=False)

    def test_chem_search(self):
        response = self.c.get('/chem_search/?chemical=dibutyl')
        #print(response.content)
        self.assertContains(response, '"Matched Data Documents": 1')
        self.assertContains(response, '"Probable Data Document matches": 55')
        self.assertNotContains(response, 'Sun_INDS_89')

        response = self.c.get('/chem_search/?chemical=ethylparaben')
        self.assertContains(response, 'SPICEBOMB3PCSGS')
        self.assertContains(response, 'The Healing Garden')

    def test_search_isolation(self):
        response = self.c.get('/chem_search/?chemical=dibutyl')
        self.assertContains(response, '"Matched Data Documents": 1')
        # remove the search term from the DSSToxSubstance records and re-index
        DSSToxSubstance.objects.filter(true_chemname='dibutyl phthalate').update(true_chemname='changed_name')
        update_index.Command().handle( using=['test_index'], interactive=False)
        
        response = self.c.get('/chem_search/?chemical=dibutyl')
        self.assertContains(response, '"Matched Data Documents": 0')
