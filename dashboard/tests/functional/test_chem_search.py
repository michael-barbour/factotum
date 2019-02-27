from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import resolve
from django.contrib.auth.models import User
from haystack.management.commands import update_index, clear_index
from haystack import connections
import time
from django.conf import settings
from dashboard.models import DSSToxLookup
from lxml import html
from dashboard.tests.loader import fixtures_standard




@override_settings(HAYSTACK_CONN='test_index')
class ChemSearchTest(TestCase):
    fixtures = fixtures_standard

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        update_index.Command().handle( remove=True, using=['test_index'],
                                            interactive=False, verbosity=0)

    @classmethod
    def tearDownClass(cls):
        clear_index.Command().handle( using=['test_index'],
                                            interactive=False, verbosity=0)
        super().tearDownClass()

    def setUp(self):
        # print('Test case setUp() method running')
        self.c = Client()
        # index_start = time.time()

        # index_elapsed = time.time() - index_start
        # print('Indexing took %s seconds' % index_elapsed)



    def test_chem_search(self):
        response = self.c.get('/chem_search/?chemical=dibutyl')
        self.assertContains(response, '"matchedDataDocuments": 2')
        self.assertContains(response, '"probableDataDocumentMatches": 56')
        self.assertNotContains(response, 'Sun_INDS_89')

        response = self.c.get('/chem_search/?chemical=ethylparaben')
        self.assertContains(response, 'SPICEBOMB3PCSGS')
        self.assertContains(response, 'The Healing Garden')

    def test_chemical_search_ui_results(self):
        response = self.client.get('/findchemical/?q=ethyl').content.decode('utf8')
        response_html = html.fromstring(response)
        self.assertIn('Sun_INDS_89',
                      response_html.xpath('string(/html/body/div[1]/div/div[2]/ol)'),
                      'The link to Sun_INDS_89 must be returned by a chemical search for "ethyl"')
