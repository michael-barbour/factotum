from django.test import TestCase, RequestFactory
from dashboard.models import DataSource
from dashboard.models import SourceType
from dashboard.models import DataGroup
from django.contrib.auth.models import User
from django.utils import timezone
from .testing_utilities import populate_test_db

class TestThroughIssue30(TestCase):
    def setUp(self):
        # Populate database
        populate_test_db()

    def test_data_group_matched_docs(self):
        # Confirm that the DataGroup with no related documents returns zero for matched_docs
        dg = DataGroup.objects.get(pk=1)
        self.assertEquals(dg.matched_docs(), 0)

        # Confirm that the DataGroup WITH related documents returns greater than zero for matched_docs
        dg = DataGroup.objects.get(pk=2)
        self.assertGreater(dg.matched_docs(), 0)
