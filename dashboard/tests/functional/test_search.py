from django.test import TestCase
from dashboard.tests.loader import load_model_objects, fixtures_standard
from dashboard.models import DataDocument
from dashboard.documents import DataDocumentDocument
from django_elasticsearch_dsl import DocType, Index


class TestSearch(TestCase):

    def setUp(self):
        """
        destroy the main index and repopulate it with the test fixture
        """
        datadocs = Index('datadocs')
        datadocs_bkp = datadocs.clone('datadocs-bkp')
        print(datadocs_bkp.__dict__)

    def test_datadoc_index(self):
        docsearch = DataDocumentDocument.search().query("match", title="Depot")
        for hit in docsearch:
            print(
                "filename : {}, title {}".format(hit.filename, hit.title)
            )