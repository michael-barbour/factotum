from django.contrib.auth.models import User
from dashboard.models import DataSource, DataGroup, DataDocument, SourceType
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

class DataGroupTest(TestCase):

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
        
        # DataGroup
        self.dg = self.create_data_group(data_source=self.ds)
        self.pdfs = self.upload_pdfs()

        # DataDocuments
        self.dds = self.create_data_documents(data_group = self.dg)
    
    def tearDown(self):
        del self.dg

    def create_source_type(self, title='msds/sds'):
        return SourceType.objects.create(title=title)

    def create_data_source(self, title='Data Source for Test', estimated_records=2, state='AT', priority='HI', typetitle='msds/sds'):
        return DataSource.objects.create(title=title, estimated_records=estimated_records, state=state, priority=priority, type=SourceType.objects.get(title=typetitle))

    def create_data_group(self, data_source, testusername = 'jdoe', name='Data Group for Test', description='Testing the DataGroup model'):
            source_csv = open('./sample_files/register_records_matching.csv','rb')              
            return DataGroup.objects.create(name=name, 
                                            description=description, data_source = data_source,
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

    def test_object_creation(self):
        self.assertTrue(isinstance(self.ds, DataSource))
        self.assertTrue(isinstance(self.dg, DataGroup))
        self.assertTrue(isinstance(self.dds, collections.Iterable))

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

       
    def test_data_source_view(self):
        response = self.client.get(reverse('data_source_detail', args=[self.ds.pk]))
        request = response.wsgi_request
        request.user = self.user
        response = data_source.data_source_detail(request, self.ds.pk)
        self.assertEqual(response.status_code, 200)

    def test_data_group_view(self):
        response = self.client.get(reverse('data_group_detail', args=[self.dg.pk]))
        request = response.wsgi_request
        request.user = self.user
        response = data_group.data_group_detail(request, self.dg.pk)
        self.assertEqual(response.status_code, 200)