import csv
import time
from lxml import html

from django.urls import resolve
from django.test import TestCase

from dashboard.tests.loader import load_model_objects, fixtures_standard
from dashboard import views
from dashboard.models import *


class DataSourceTestWithFixtures(TestCase):
    fixtures = fixtures_standard
    
    def setUp(self):
        self.client.login(username='Karyn', password='specialP@55word')

    def test_extracted_counts(self):
        response = self.client.get('/datasources/').content.decode('utf8')
        self.assertIn('Extracted', response,
                      'The Extracted document count should be in the page after ticket 758')
        response_html = html.fromstring(response)
        ext_table_count = int(response_html.xpath("//*[@id='sources']/tbody/tr[contains(., 'Airgas')]/td[4]")[0].text)
        ext_orm_count = ExtractedText.objects.filter(data_document__data_group__data_source__title='Airgas').count()
        self.assertEqual(ext_table_count, ext_orm_count,
                         'The number of extracted records shown for Airgas should match what the ORM returns')

