from django.test import TestCase
from lxml import html

from dashboard.tests.loader import load_model_objects

from django.urls import reverse

class PUCTagTest(TestCase):

    def setUp(self):
        self.objects = load_model_objects()
        self.client.login(username='SuperKaryn', password='specialP@55word')

    # def test_admin_product_attribute_puc_column_exists(self):
    #     response_url = reverse('admin:dashboard_producttag_changelist')
    #     response = self.client.get(response_url)
    #     response_html = html.fromstring(response.content.decode('utf8'))
    #     self.assertIn('PUC', response_html.xpath('string(/html/body/div[1]/div[3]/div/div/form/div[2]/table/thead/tr/th[3]/div[1])'),
    #                   'The column PUC should exist on the Product Attributes admin table')
