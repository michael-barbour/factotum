from django.test import TestCase

from dashboard.models import ProductAttribute, ProductToAttribute, PUC
from dashboard.tests.loader import load_model_objects

class ProductToAttributeTest(TestCase):

    def setUp(self):
        self.objects = load_model_objects()

    def test_product_attribute_exists(self):
        a = ProductAttribute.objects.create(title='tang', type='ms')
        self.assertFalse(self.objects.p.productattribute_set.exists())
        self.assertEqual(len(ProductToAttribute.objects.all()), 0,
                    ("There should be no Product linked to ProductAttribute"))
        c = ProductToAttribute.objects.create(product=self.objects.p,
                                              product_attribute=a)
        self.assertTrue(self.objects.p.productattribute_set.exists())
        self.assertEqual(len(ProductToAttribute.objects.all()), 1,
                        ("There should be Product linked to ProductAttribute"))

    def test_product_attribute_puc(self):
        puc = PUC.objects.create(gen_cat = 'Flavorings', last_edited_by=self.objects.user)
        a = ProductAttribute.objects.create(title='tang', type='ms', PUC=puc)
        self.assertTrue(a.PUC == puc)

