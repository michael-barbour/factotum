from lxml import html

from django.test import TestCase

from dashboard.models import DSSToxLookup
from dashboard.tests.loader import fixtures_standard


class DSSToxDetail(TestCase):

    fixtures = fixtures_standard

    def setUp(self):
        self.client.login(username='Karyn', password='specialP@55word')

    def test_dsstox_detail(self):
        dss = next(dss for dss in DSSToxLookup.objects.all() if dss.puc_count>0)
        response = self.client.get(f'/dsstox_lookup/{dss.sid}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dss.puc_count, len(response.context['pucs']),
                            f'DSSTox pk={dss.pk} should have {dss.puc_count} '
                             'PUCs in the context')
        link = ('https://comptox.epa.gov/dashboard/dsstoxdb/results?search='
                f'{dss.sid}')
        self.assertIn(link,response.content.decode('utf-8'))
        dss = next(dss for dss in DSSToxLookup.objects.all() if dss.puc_count<1)
        response = self.client.get(f'/dsstox_lookup/{dss.sid}/')
        self.assertEqual(dss.puc_count, len(response.context['pucs']),
                            f'DSSTox pk={dss.pk} should have {dss.puc_count} '
                             'PUCs in the context')
        
        # response_html = html.fromstring(response.content.decode('utf8'))
        # response_html.xpath('string(/html/body/div[1]/div[2]/div/div[1]/div/div[2])')
        # import pdb; pdb.set_trace()
        # print(response.content)
