from django.test import TestCase, override_settings
from dashboard.tests.loader import *
from dashboard.models import DataGroup
from dashboard.views.data_group import DataGroupForm


@override_settings(ALLOWED_HOSTS=['testserver'])
class DataGroupFormTest(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.client.login(username='Karyn', password='specialP@55word')

    def test_detail_form_url(self):
        self.assertTrue(DataGroupForm().fields['url'],
                        'DataGroupForm should include the url')

        dg = DataGroup.objects.get(pk=6)
        response = self.client.post(f'/datagroup/edit/{dg.pk}/',
                                    {'name': dg.name,
                                    'url': 'http://www.epa.gov',
                                    'group_type': dg.group_type_id,
                                    'downloaded_by': dg.downloaded_by_id,
                                    'downloaded_at': dg.downloaded_at,
                                    'data_source': dg.data_source_id})
        dg.refresh_from_db()
        dg = DataGroup.objects.get(pk=dg.pk)
        self.assertEqual(dg.url, 'http://www.epa.gov',
                     f'DataDocument {dg.pk} should have the url "http://www.epa.gov"')


