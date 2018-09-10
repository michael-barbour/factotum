from django.test import TestCase, override_settings

from dashboard.tests.loader import *

class DataGroupTest(TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/datagroups/')
        # print(response)
        # print(response.status_code)
        self.assertEqual(response.status_code, 302,
                                        "User should be redirected to login")
        # print(response.url)
        self.assertEqual(response.url, '/login/?next=/datagroups/',
                                        "User should be sent to login page")
        # print(type(response))

        #
        # self.assertTrue(DataGroupForm().fields['url'],
        #                 'DataGroupForm should include the url')
        #
        # dg = DataGroup.objects.get(pk=6)
        # response = self.client.post(f'/datagroup/edit/{dg.pk}/',
        #                             {'name': dg.name,
        #                             'url': 'http://www.epa.gov',
        #                             'group_type': dg.group_type_id,
        #                             'downloaded_by': dg.downloaded_by_id,
        #                             'downloaded_at': dg.downloaded_at,
        #                             'data_source': dg.data_source_id})
        # dg.refresh_from_db()
        # dg = DataGroup.objects.get(pk=dg.pk)
        # self.assertEqual(dg.url, 'http://www.epa.gov',
        #              f'DataDocument {dg.pk} should have the url "http://www.epa.gov"')
