from django.test import Client
from dashboard.tests.loader import *
import requests

class TestChemicalSearch(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.factory = RequestFactory()
        self.client.login(username='Karyn', password='specialP@55word')

    def test_search_api(self):
        """
        The correct JSON comes back from the elasticsearch server
        """
        response = requests.get('http://127.0.0.1:9200/')
        self.assertTrue(response.ok)
        
        response = requests.get('http://127.0.0.1:9200/factotum_chemicals/_search?q=ethylparaben')
        #print(response.content)
        self.assertIn('DTXSID9022528', str(response.content))

    def test_results_page(self):
        """
        The result page returns the correct content
        """
        response = self.client.get('/search/es_chemicals/?q=ethylparaben')
        pdf_url = "/media/3dada08f-91aa-4e47-9556-e3e1a23b1d7e/pdf/document_127870.pdf"
        self.assertIn(pdf_url, str(response.content))
        #print(response.content)
        
        prod_count_html = "<dt>Product count:</dt>\n<dd>2</dd>"
        self.assertIn(prod_count_html, str(response.content))
