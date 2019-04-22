from django.test import TestCase
from dashboard.tests.loader import load_model_objects, fixtures_standard
from dashboard.search_indexes.documents.factotum_chemicals import FactotumChemicalDocument
from django_elasticsearch_dsl import DocType, Index
import pprint


class TestSearch(TestCase):

    INDEX_SUFFIX = '-test'
    testindexname = f'factotum_chemicals%s' % INDEX_SUFFIX

    def setUp(self):
        """
        clone indexes and populate them with fixture data
        """
        factotum_chemicals = Index('factotum_chemicals')

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(factotum_chemicals.get_mapping())

        pp.pprint(factotum_chemicals.get_settings())

        if Index(self.testindexname).exists():
            Index(self.testindexname).delete()
        factotum_chemicals_test = factotum_chemicals.clone(self.testindexname)
        factotum_chemicals_test.create()

        factotum_chemicals_test.settings(read_only_allow_delete="false")
        # at this point, we need to tell elasticsearch-dsl that the objects being added 
        # to the local_factotum_test database should be indexed into the datadocs-test index
        load_model_objects()
        

    def tearDown(self):
        """
        remove the test indexes
        """
        factotum_chemicals_test = Index(self.testindexname)
        factotum_chemicals_test.delete()

    def test_chemicals_index(self):
        chemsearch = FactotumChemicalDocument.search(index=self.testindexname).query("match", title="phthalate")

        #print(FactotumChemicalDocument.search(index=self.testindexname).__dict__)
        for hit in chemsearch:
            print(
                "true_chemname : {}, raw_chem_name {}".format(hit.true_chemname, hit.raw_chem_name)
            )