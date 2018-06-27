from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .loader import load_model_objects
from dashboard.models import ExtractedText

class ModelsTest(TestCase):

    def setUp(self):

        self.objects = load_model_objects()
        self.client.login(username='Karyn', password='specialP@55word')

    def test_extracted_doc_date_validation(self):
        # check validation for year
        text = ExtractedText(doc_date= '2027-04-13',
                                data_document=self.objects.doc,
                                extraction_script=self.objects.script)
        self.assertRaises(ValidationError, text.clean)
        # check validation for month
        text = ExtractedText(doc_date= '2010-24-13',
                                data_document=self.objects.doc,
                                extraction_script=self.objects.script)
        self.assertRaises(ValidationError, text.clean)
        # check validation for day
        text = ExtractedText(doc_date= '2010-04-47',
                                data_document=self.objects.doc,
                                extraction_script=self.objects.script)
        self.assertRaises(ValidationError, text.clean)
        # check validation for proper length string
        text = ExtractedText(doc_date= '2010-04-1300',
                                data_document=self.objects.doc,
                                extraction_script=self.objects.script)
        self.assertRaises(ValidationError, text.clean)
        # check validation not thrown if doc_date is null
        text = ExtractedText(data_document=self.objects.doc,
                                extraction_script=self.objects.script)
        try:
            text.clean()
        except ValidationError:
            self.fail("clean() raised ExceptionType unexpectedly!")

    def test_extracted_text_qa_notes(self):
        text = ExtractedText(doc_date= '2018-04-13',
                                            data_document=self.doc,
                                            extraction_script=self.script)
        text.qa_status = ExtractedText.APPROVED_WITH_ERROR
        with self.assertRaises(ValidationError):
            text.clean()
        text.qa_notes = "Some notes belong here if qa_status is APPROVED_WITH_ERROR"
        self.assertRaises(ValidationError, text.clean)

    def test_validation_errors_appear_in_qa_template(self):
        extext = ExtractedText(doc_date= '2018-04-13',
                                            data_document=self.doc,
                                            extraction_script=self.script)
        chem_formset = ChemFormSet(instance=extext, prefix='chemicals')
        context = {
            'extracted_text': extext,
            'doc': self.doc, 
            'script': self.script, 
            'chem_formset': chem_formset, 
            'stats': stats, 
            'nextid': nextid,
            'chem_formset': chem_formset,
            'notesform': notesform,
            }
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = "You can't have an empty list item"
        self.assertContains(response, expected_error)