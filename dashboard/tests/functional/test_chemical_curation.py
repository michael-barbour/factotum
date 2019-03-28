from django.test import TestCase
from dashboard.tests.loader import fixtures_standard


class ChemicalCurationTests(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.client.login(username='Karyn', password='specialP@55word')

    def test_chemical_curation_page(self):
        """
        Ensure there is a chemical curation page
        :return: a 200 status code
        """
        response = self.client.get('/chemical_curation/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Download Uncurated Chemicals')
