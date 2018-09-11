from django.test import TestCase, override_settings
from dashboard.tests.loader import *
from dashboard.views.product_curation import ProductForm, ProductViewForm
from lxml import html


@override_settings(ALLOWED_HOSTS=['testserver'])
class TestProductDetail(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.client.login(username='Karyn', password='specialP@55word')

    def test_product_delete(self):
        self.assertTrue(Product.objects.get(pk=11),
                         'Product 11 should exist')
        response = self.client.get(f'/product/delete/11/')
        self.assertFalse(Product.objects.filter(pk=11),
                         'Product 11 should have been deleted')

    def test_product_update(self):
        p = Product.objects.get(pk=11)
        response = self.client.post(f'/product/edit/11/',
                                    {'title': 'x',
                                     'manufacturer': '',
                                     'brand_name': '',
                                     'short_description': 'none',
                                     'long_description': 'none',
                                     'size': '',
                                     'color': '',
                                     'model_number': '2'})
        p.refresh_from_db()
        self.assertEqual(p.title, 'x',
                         'Product 11 should have the title "x"')


    def test_add_puc(self):
        p = Product.objects.get(pk=14)
        response = self.client.get(f'/product/{str(p.pk)}/').content.decode('utf8')
        response_html = html.fromstring(response)

        self.assertTrue(p.get_uber_puc() == None,
                        'Product should not have an assigned PUC')

        self.assertIn('Assign PUC',
                      response_html.xpath('string(//*[@id="button_assign_puc"]/text())'),
                      'There should be an Assign PUC button for this product')

        response = self.client.post(f'/product_puc/{str(p.pk)}/',
                                    {'puc': '96' })

        p.refresh_from_db()

        self.assertTrue(p.get_uber_puc() != None,
                        'Product should now have an assigned PUC')

        response = self.client.get('/product/{str(p.pk)}/').content.decode('utf8')
        response_html = html.fromstring(response)

        self.assertNotIn('Assign PUC',
                      response_html.xpath('string(//*[@id="button_assign_puc"]/text())'),
                      'There should not be an Assign PUC button for this product')




