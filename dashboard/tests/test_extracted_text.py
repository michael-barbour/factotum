from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from dashboard.models import (SourceType, DataSource, DataGroup, DataDocument,
                              Script, ExtractedText, ExtractedChemical)

class ModelsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='Karyn', email='jon.doe@epa.gov',
            password='specialP@55word')

        self.client.login(username='Karyn', password='specialP@55word')

        self.st = SourceType.objects.create(title='msds/sds')

        self.ds = DataSource.objects.create(title='Data Source for Test',
                                            estimated_records=2, state='AT',
                                            priority='HI', type=self.st)

        self.script = Script.objects.create(title='Test Title',
                                        url='http://www.epa.gov/',
                                        qa_begun=False, script_type='DL')

        self.dg = DataGroup.objects.create(name='Data Group for Test',
                                    description='Testing the DataGroup model',
                                    data_source = self.ds,
                                    download_script=self.script,
                                    downloaded_by=self.user,
                                    downloaded_at=timezone.now(),
                                    csv='register_records_matching.csv')

        self.doc = DataDocument.objects.create(data_group=self.dg,
                                               source_type=self.st)

    def test_extracted_doc_date_validation(self):
        # check validation for year
        text = ExtractedText(doc_date= '2027-04-13',
                                            data_document=self.doc,
                                            extraction_script=self.script)
        self.assertRaises(ValidationError, text.clean)
        # check validation for month
        text = ExtractedText(doc_date= '2010-24-13',
                                            data_document=self.doc,
                                            extraction_script=self.script)
        self.assertRaises(ValidationError, text.clean)
        # check validation for day
        text = ExtractedText(doc_date= '2010-04-47',
                                            data_document=self.doc,
                                            extraction_script=self.script)
        self.assertRaises(ValidationError, text.clean)
        # check validation for proper length string
        text = ExtractedText(doc_date= '2010-04-1300',
                                            data_document=self.doc,
                                            extraction_script=self.script)
        self.assertRaises(ValidationError, text.clean)
        # check validation not thrown if doc_date is null
        text = ExtractedText(data_document=self.doc,
                             extraction_script=self.script)
        try:
            text.clean()
        except ValidationError:
            self.fail("clean() raised ExceptionType unexpectedly!")
