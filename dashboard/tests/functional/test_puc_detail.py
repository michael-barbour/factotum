from lxml import html

from django.test import TestCase, override_settings

from dashboard.models import *
from dashboard.tests.loader import *


@override_settings(ALLOWED_HOSTS=['testserver'])
class TestPUCDetail(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.client.login(username='Karyn', password='specialP@55word')

    def test_puc_not_specified(self):
        response = self.client.get('/puc/20/')
