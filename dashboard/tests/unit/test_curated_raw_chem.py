from django.test import TestCase
from django.contrib.auth.models import User
from dashboard.tests.loader import *
from dashboard.models import DSSToxLookup, RawChem


# model test
class CuratedChemTest(TestCase):
    fixtures = fixtures_standard

    def test_sid_property(self):
        rc = RawChem.objects.get(id=3)
        rc.rid = 'DTXRID7485239'
        self.assertFalse(rc.sid)
        dss = DSSToxLookup.objects.get(id=13)
        # link the RawChem record to the DSSToxLookup record
        rc.curated_chemical = dss
        rc.save()
        self.assertEqual(rc.sid, dss.sid)
        # Remove the link
        rc.curated_chemical = None
