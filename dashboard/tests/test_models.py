from django.contrib.auth.models import User
from dashboard.models import DataSource, DataGroup, DataDocument, SourceType
from django.test import TestCase, RequestFactory
from django.utils import timezone   

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


    def create_source_type(self, title='msds/sds'):
        return SourceType.objects.create(title=title)

    def create_data_source(self, title='Data Source for Test', estimated_records=2, state='AT', priority='HI', typetitle='msds/sds'):
        return DataSource.objects.create(title=title, estimated_records=estimated_records, state=state, priority=priority, type=SourceType.objects.get(title=typetitle))

    def create_data_group(self, data_source, testusername = 'jdoe', name='Data Group for Test', description='Testing the DataGroup model', csv='./sample_files/register_records_matching.csv'):
            return DataGroup.objects.create(name=name, description=description, data_source = data_source,
                                            downloaded_by=User.objects.get(username=testusername), downloaded_at=timezone.now(),
                                            csv=csv)

    def test_object_creation(self):
        self.assertTrue(isinstance(self.ds, DataSource))
        self.assertTrue(isinstance(self.dg, DataGroup))

    def test_object_properties(self):
        # Test properties of objects
        self.assertEqual(self.ds.__str__(), self.ds.title)
        self.assertEqual(self.dg.__str__(), self.dg.name)
        self.assertEqual(self.dg.dgurl(), self.dg.name.replace(' ', '_'))