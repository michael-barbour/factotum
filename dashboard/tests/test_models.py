from django.contrib.auth.models import User
from dashboard.models import DataSource, DataGroup, DataDocument, SourceType, ExtractedText, ExtractedChemical, DSSToxSubstance, Script
from dashboard.views import data_source, data_group
from django.test import TestCase, RequestFactory
from django.utils import timezone
import os
import csv
import collections
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    f.closed
    return i + 1


class ModelsTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jdoe', email='jon.doe@epa.gov', password='Sup3r_secret')
        self.client.login(username='jdoe', password='Sup3r_secret')

        # SourceType
        self.st = self.create_source_type()

        # DataSource
        self.ds = self.create_data_source()

        # Script, type DL
        self.dl = self.create_download_script(script_type='DL')

        # DataGroup
        self.dg = self.create_data_group(data_source=self.ds, download_script=self.dl)
        self.pdfs = self.upload_pdfs()

        # DataDocuments
        self.dds = self.create_data_documents(data_group = self.dg)

        # Script, type EX
        self.ex = self.create_extraction_script(script_type='EX')

        # ExtractedText
        self.et = self.create_extracted_text(data_documents=self.dds, extraction_script=self.ex)

        # ExtractedChemical
        self.ec = self.create_extracted_chemical(extracted_text=self.et)

        # DSSToxSubstance
        self.dsstox = self.create_dsstox_substance(extracted_chemical=self.ec)

    def tearDown(self):
        del self.dg

    def create_source_type(self, title='msds/sds'):
        return SourceType.objects.create(title=title)

    def create_data_source(self, title='Data Source for Test', estimated_records=2, state='AT', priority='HI', typetitle='msds/sds'):
        return DataSource.objects.create(title=title, estimated_records=estimated_records, state=state, priority=priority, type=SourceType.objects.get(title=typetitle))

    def create_download_script(self, script_type, title='Test Title', url='http://www.epa.gov/', qa_begun=False):
        return Script.objects.create(title=title, url=url, qa_begun=qa_begun, script_type=script_type)

    def create_data_group(self, data_source, download_script, testusername = 'jdoe', name='Data Group for Test', description='Testing the DataGroup model'):
            source_csv = open('./sample_files/register_records_matching.csv','rb')
            return DataGroup.objects.create(name=name,
                                            description=description, data_source = data_source,
                                            download_script=download_script,
                                            downloaded_by=User.objects.get(username=testusername),
                                            downloaded_at=timezone.now(),
                                            csv=SimpleUploadedFile('register_records_matching.csv', source_csv.read() )
                                            )

    def upload_pdfs(self):
        store = settings.MEDIA_URL + self.dg.dgurl()
        pdf1_name = '0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf'
        pdf2_name = '0c68ab16-2065-4d9b-a8f2-e428eb192465.pdf'
        local_pdf = open('./sample_files/' + pdf1_name, 'rb')
        fs = FileSystemStorage(store + '/pdf')
        fs.save(pdf1_name, local_pdf)
        local_pdf = open('./sample_files/' + pdf2_name, 'rb')
        fs = FileSystemStorage(store + '/pdf')
        fs.save(pdf2_name, local_pdf)
        return [pdf1_name, pdf2_name]

    def create_data_documents(self, data_group):
        dds = []
        #pdfs = [f for f in os.listdir('/media/' + self.dg.dgurl() + '/pdf') if f.endswith('.pdf')]
        #pdfs
        with open(data_group.csv.path) as dg_csv:
            table = csv.DictReader(dg_csv)
            text = ['DataDocument_id,' + ','.join(table.fieldnames)+'\n']
            errors = []
            count = 0
            for line in table: # read every csv line, create docs for each
                count+=1
                if line['filename'] == '':
                    errors.append(count)
                if line['title'] == '': # updates title in line object
                    line['title'] = line['filename'].split('.')[0]
                dd = DataDocument.objects.create(filename=line['filename'],
                    title=line['title'],
                    product_category=line['product'],
                    url=line['url'],
                    matched = line['filename'] in self.pdfs,
                    data_group=data_group)
                dds.append(dd)
            return dds

    def create_extraction_script(self, script_type, title='Test Title', url='http://www.epa.gov/', qa_begun=False):
        return Script.objects.create(title=title, url=url, qa_begun=qa_begun, script_type=script_type)

    def create_extracted_text(self, data_documents, extraction_script):
        return ExtractedText.objects.create(data_document=data_documents[0], record_type='Test Record Type', prod_name='Test Prod Name',
                                            doc_date='TstDocDate', rev_num='Test Rev Num', extraction_script=extraction_script, qa_checked=False)

    def create_extracted_chemical(self, extracted_text, cas='Test CAS', chem_name='Test Chem Name', raw_min_comp='Test Raw Min Comp',
                                  raw_max_comp='Test Raw Max Comp', units='Test Units', report_funcuse='Test Report Funcuse'):
        return ExtractedChemical.objects.create(extracted_text=extracted_text, cas=cas, chem_name=chem_name, raw_min_comp=raw_min_comp,
                                                raw_max_comp=raw_max_comp, units=units, report_funcuse=report_funcuse)

    def create_dsstox_substance(self, extracted_chemical, true_cas='Test True CAS',
                                true_chemname='Test True Chem Name', rid='Test RID', sid='Test SID'):
        return DSSToxSubstance.objects.create(extracted_chemical=extracted_chemical, true_cas=true_cas,
                                              true_chemname=true_chemname, rid=rid, sid=sid)

    def test_object_creation(self):
        self.assertTrue(isinstance(self.ds, DataSource))
        self.assertTrue(isinstance(self.dg, DataGroup))
        self.assertTrue(isinstance(self.dds, collections.Iterable))
        self.assertTrue(isinstance(self.ex, Script))
        self.assertTrue(isinstance(self.et, ExtractedText))
        self.assertTrue(isinstance(self.ec, ExtractedChemical))
        self.assertTrue(isinstance(self.dsstox, DSSToxSubstance))

    def test_object_properties(self):
        # Test properties of objects
        # DataSource
        self.assertEqual(self.ds.__str__(), self.ds.title)

        # DataGroup
        self.assertEqual(self.dg.__str__(), self.dg.name)
        self.assertEqual(self.dg.dgurl(), self.dg.name.replace(' ', '_'))
        # The number of rows in the DataGroup's uploaded csv should match the rows in the local copy
        csv_there = file_len(self.dg.csv.path)
        csv_here  = file_len('./sample_files/register_records_matching.csv')
        self.assertEqual(csv_there, csv_here)

        # DataDocuments
        #The number of data documents created should match the number of rows in the csv file minus the header
        self.assertEqual(len(self.dds) , csv_there - 1)
        # Confirm that one of the data documents appears in the data group show page
        dg_response = self.client.get('/datagroup/' + str(self.dg.pk), follow=True)
        self.assertIn(b'NUTRA', dg_response.content)
        self.assertEqual(len(self.pdfs), 2)
        # Confirm that the two data documents in the csv file are matches to the pdfs via their file names
        self.assertEqual(self.dg.matched_docs(), 2)
        # Test a link to an uploaded pdf
        good_url = b'Data_Group_for_Test/pdf/0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf'
        self.assertIn(good_url, dg_response.content)

        # ExtractionScript
        self.assertEqual(self.ex.__str__(), 'Test Title')

        # ExtractedText
        self.assertEqual(self.et.__str__(), 'Test Prod Name')

        # ExtractedChemical
        self.assertEqual(self.ec.__str__(), 'Test Chem Name')

        #DSSToxSubstance
        self.assertEqual(self.dsstox.__str__(), self.ec.__str__())
