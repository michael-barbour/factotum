from django.test import Client
from django.test import TestCase, override_settings

class TestApprovalView(TestCase):
    fixtures = ['00_superuser.yaml','01_lookups.yaml',
                '02_datasource.yaml','03_datagroup.yaml',
                '04_productcategory.yaml','05_product_lite.yaml',
                '06_datadocument_lite.yaml','07_script.yaml',
                '08_extractedtext_lite.yaml','09_productdocument_lite.yaml',
                '10_extractedchemical.yaml']
    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_other_domain(self):
        response = self.client.post('/login/', {'username': 'karyn', 'password': 'specialP@55word'})
        print(response.status_code)
        print(response)
    




