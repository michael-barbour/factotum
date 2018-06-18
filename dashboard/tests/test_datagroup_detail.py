from django.test import TestCase
from .loader import load_model_objects
from dashboard.models import DataGroup
from django.core.files.uploadedfile import SimpleUploadedFile

class DataGroupTest(TestCase):

    def setUp(self):
        self.objects = load_model_objects()
        self.client.login(username='Karyn', password='specialP@55word')

    def test_detail_form_loads(self):
        pk = DataGroup.objects.first().pk
        response = self.client.get(f'/datagroup/{pk}')
        self.assertFalse(self.objects.doc.matched,(
                    'Document should start w/ matched False'))
        self.assertFalse(self.objects.doc.extracted,(
                    'Document should start w/ extracted False'))
        self.assertTrue(response.context['include_upload'], (
                    'UploadForm should be included in the page!'))
        self.assertFalse(response.context['include_extract'], (
                    'ExtractForm should not be included in the page!'))
        self.objects.doc.matched = True
        self.objects.doc.save()
        response = self.client.get(f'/datagroup/{pk}')
        self.assertFalse(response.context['include_upload'], (
                    'UploadForm should not be included in the page!'))
        self.assertTrue(response.context['include_extract'], (
                    'ExtractForm should be included in the page!'))
        self.objects.doc.extracted = True
        self.objects.doc.save()
        response = self.client.get(f'/datagroup/{pk}')
        self.assertFalse(response.context['include_upload'], (
        'UploadForm should not be included in the page!'))
        self.assertFalse(response.context['include_extract'], (
        'ExtractForm should not be included in the page!'))


# include_extract


# content = b'datagroup,name,hair'
# f = SimpleUploadedFile("file.txt", content)
# response = self.client.post(f'/datagroup/{pk}',
#                         {'attachment':f, 'extract_button': ['Submit']})
