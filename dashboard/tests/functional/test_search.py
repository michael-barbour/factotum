from django.test import TestCase
from dashboard.tests.loader import load_model_objects, fixtures_standard
from dashboard.models import DataDocument
from dashboard.documents import DataDocumentDocument

class TestSearch(TestCase):
    fixtures = fixtures_standard

    def test_datadoc_index():
        docsearch = DataDocumentDocument.search().query("match", title="Depot")
        for hit in docsearch:
            print(
                "filename : {}, title {}".format(hit.filename, hit.title)
            )