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

class TestRawChemSubclasses(TestCase):
    fixtures = fixtures_standard

    def test_get_data_documents(self):
        ''' Traversing the subclasses
            and confirming that each subclass's data document matches what is returned by its
            related RawChem record's get_data_document() method. 
         '''
        for ec in ExtractedChemical.objects.all():
            rc=ec.rawchem_ptr
            self.assertEqual(ec.data_document , rc.get_data_document(),
                    'The ExtractedChemical object and RawChem object should hae the same datadocument')
        for efu in ExtractedFunctionalUse.objects.all():
            rc=efu.rawchem_ptr
            self.assertEqual(efu.data_document , rc.get_data_document(),
                    'The ExtractedFunctionalUse object and RawChem object should hae the same datadocument')
        for elp in ExtractedListPresence.objects.all():
            rc=elp.rawchem_ptr
            self.assertEqual(elp.data_document , rc.get_data_document(),
                    'The ExtractedListPresence object and RawChem object should hae the same datadocument')