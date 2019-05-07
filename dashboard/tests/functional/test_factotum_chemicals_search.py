from django.test import TestCase
from django.test.client import Client
from lxml import html

from django.urls import resolve
from django.contrib.auth.models import User
from dashboard.tests.loader import fixtures_standard


class ChemicalSearchTest(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.c = Client()

    def test_search_results(self):
        response = self.c.get('search/es_chemicals/?q=alcohol')
        print(response.GET)
        