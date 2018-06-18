from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from dashboard.models import (SourceType, DataSource, DataGroup, DataDocument,
                              Script, ExtractedText, Product, ProductToPUC, PUC)

class ModelsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='Karyn', email='jon.doe@epa.gov',
            password='specialP@55word')

        self.client.login(username='Karyn', password='specialP@55word')

        self.st = SourceType.objects.create(title='msds/sds')

        self.ds = DataSource.objects.create(title='Data Source for Test',
                                            estimated_records=2, state='AT',
                                            priority='HI', type=self.st)

        self.script = Script.objects.create(title='Test Title',
                                        url='http://www.epa.gov/',
                                        qa_begun=False, script_type='DL')

        self.dg = DataGroup.objects.create(name='Data Group for Test',
                                    description='Testing the DataGroup model',
                                    data_source = self.ds,
                                    download_script=self.script,
                                    downloaded_by=self.user,
                                    downloaded_at=timezone.now(),
                                    csv='register_records_matching.csv')

        self.doc = DataDocument.objects.create(data_group=self.dg,
                                               source_type=self.st)

        self.p = Product.objects.create(data_source=self.ds,
                                          upc='Test UPC for ProductToPUC')

        self.puc = PUC.objects.create(gen_cat='Test General Category',
                                      prod_fam='Test Product Family',
                                      prod_type='Test Product Type',
                                      last_edited_by=self.user)


    def test_uber_puc(self):
        # Test that when the product has no assigned PUC, the getter returns
        # None
        self.assertTrue(self.p.get_uber_product_to_puc() == None)
        
        self.puc = ProductToPUC.objects.create(product=self.p,
                                        PUC=self.puc,
                                        puc_assigned_usr=self.user)

        # Test that the get_uber_product_to_puc method returns expected values
        uber_ppuc = self.p.get_uber_product_to_puc()
        self.assertTrue(uber_ppuc.puc_assigned_usr.username == 'Karyn')

        uber_puc = self.p.get_uber_puc()
        self.assertFalse("Test General Category" not in str(uber_puc))
