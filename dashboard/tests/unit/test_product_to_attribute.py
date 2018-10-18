from django.test import TestCase

from dashboard.models import PUCTag, ProductToTag, PUC
from dashboard.tests.loader import load_model_objects

class ProductToTagTest(TestCase):

    def setUp(self):
        self.objects = load_model_objects()

    def test_product_attribute_exists(self):
        a = PUCTag.objects.create(title='tang', type='ms')
        self.assertFalse(self.objects.p.producttag_set.exists())
        self.assertEqual(len(ProductToTag.objects.all()), 0,
                    ("There should be no Product linked to PUCTag"))
        c = ProductToTag.objects.create(product=self.objects.p,
                                              puc_tag=a)
        self.assertTrue(self.objects.p.producttag_set.exists())
        self.assertEqual(len(ProductToTag.objects.all()), 1,
                        ("There should be Product linked to PUCTag"))


