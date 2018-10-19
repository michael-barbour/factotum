from django.test import TestCase

from dashboard.models import PUCTag, ProductToTag, PUC
from dashboard.tests.loader import load_model_objects

class ProductToTagTest(TestCase):

    def setUp(self):
        self.objects = load_model_objects()

    def test_product_tag_exists(self):
        t = PUCTag.objects.create(name='tang', slug='tang')
        # self.assertFalse(self.objects.p.tag_set.exists())
        self.assertEqual(len(ProductToTag.objects.all()), 0,
                    ("There should be no Product linked to PUCTag"))
        c = ProductToTag.objects.create(content_object=self.objects.p,
                                              tag=t)
        # self.assertTrue(self.objects.p.tag_set.exists())
        self.assertEqual(len(ProductToTag.objects.all()), 1,
                        ("There should be Product linked to PUCTag"))


