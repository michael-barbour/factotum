from django.test import TestCase
from dashboard.tests.loader import load_model_objects, fixtures_standard
from dashboard.models import DataDocument
from dashboard.documents import DataDocumentDocument
from django_elasticsearch_dsl import DocType, Index

class TestSearch(TestCase):

    INDEX_SUFFIX = '-test'
    testindexname = f'datadocs%s' % INDEX_SUFFIX

    def setUp(self):
        """
        clone indexes and populate them with fixture data
        """
        datadocs = Index('datadocs')
        if Index(self.testindexname).exists():
            Index(self.testindexname).delete()
        datadocs_test = datadocs.clone(self.testindexname)
        datadocs_test.create()

        datadocs_test.settings(read_only_allow_delete="false")
        # at this point, we need to tell elasticsearch-dsl that the objects being added 
        # to the local_factotum_test database should be indexed into the datadocs-test index
        load_model_objects()
        

    def tearDown(self):
        """
        remove the test indexes
        """
        datadocs_test = Index(self.testindexname)
        datadocs_test.delete()

    def test_datadoc_index(self):
        docsearch = DataDocumentDocument.search(index=self.testindexname).query("match", title="Depot")

        print(DataDocumentDocument.search(index=self.testindexname).__dict__)
        for hit in docsearch:
            print(
                "filename : {}, title {}".format(hit.filename, hit.title)
            )