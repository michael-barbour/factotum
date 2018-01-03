from django.contrib.auth.models import User
from dashboard.models import DataSource, DataGroup, DataDocument, SourceType
from django.test import TestCase, RequestFactory
from django.utils import timezone
import os 
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

class DataGroupTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jdoe', email='jon.doe@epa.gov', password='Sup3r_secret')

        # SourceType
        self.st = self.create_source_type()

        # DataSource
        self.ds = self.create_data_source()
        
        # DataGroup
        self.dg = self.create_data_group(data_source=self.ds)

        # DataDocuments
        #self.dds = self.create_data_documents(data_group = self.dg)

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

    def create_data_documents(self, data_group):
        info = [x.decode('ascii',
                'ignore') for x in data_group.csv.path.readlines()]
        table = data_group.csv.DictReader(info)
        text = ['DataDocument_id,' + ','.join(table.fieldnames)+'\n']
        errors = []
        count = 0
        for line in table: # read every csv line, create docs for each
            count+=1
            if line['filename'] == '':
                errors.append(count)
            if line['title'] == '': # updates title in line object
                line['title'] = line['filename'].split('.')[0]
            DataDocument.objects.create(filename=line['filename'],
                title=line['title'],
                product_category=line['product'],
                url=line['url'],
                data_group=data_group)

    def test_object_creation(self):
        self.assertTrue(isinstance(self.ds, DataSource))
        self.assertTrue(isinstance(self.dg, DataGroup))

    def test_object_properties(self):
        # Test properties of objects
        # DataSource
        self.assertEqual(self.ds.__str__(), self.ds.title)
        # DataGroup
        self.assertEqual(self.dg.__str__(), self.dg.name)
        self.assertEqual(self.dg.dgurl(), self.dg.name.replace(' ', '_'))
        # The DataGroup's uploaded csv 
        csv_there = file_len(self.dg.csv.path)
        csv_here  = file_len('./sample_files/register_records_matching.csv')
        self.assertEqual(csv_there, csv_here)
        
        