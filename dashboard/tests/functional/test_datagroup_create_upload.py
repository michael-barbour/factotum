import os
import io

from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            TemporaryUploadedFile)

from factotum import settings
from dashboard import views
from dashboard.models import *

class RegisterRecordsTest(TestCase):
    fixtures = ['00_superuser.yaml','01_lookups.yaml',
                '02_datasource.yaml','07_script.yaml']

    def setUp(self):
        self.factory = RequestFactory()
        self.client.login(username='Karyn', password='specialP@55word')

    def test_datagroup_create(self):
        csv_string = ("filename,title,document_type,url,organization\n"
                "0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf,NUTRA NAIL,1,, \n"
                "0c68ab16-2065-4d9b-a8f2-e428eb192465.pdf,Body Cream,1,, \n")
        data = io.StringIO(csv_string)
        sample_csv = InMemoryUploadedFile(data,
                                            field_name='csv',
                                            name='register_records.csv',
                                            content_type='text/csv',
                                            size=len(csv_string),
                                            charset='utf-8')
        form_data= {'name': ['Walmart MSDS Test Group'],
                    'description': ['test data group'],
                    'group_type': ['5'],
                    'downloaded_by': [str(User.objects.get(username='Karyn').pk)],
                    'downloaded_at': ['08/02/2018'],
                    'download_script': ['1'],
                    'data_source': ['10']}
        request = self.factory.post(path='/datagroup/new', data=form_data)
        request.FILES['csv'] = sample_csv
        request.user = User.objects.get(username='Karyn')
        request.session={}
        request.session['datasource_title'] = 'Walmart'
        request.session['datasource_pk'] = 10
        print('POST request for creating data group')
        print(request.POST)
        resp = views.data_group_create(request=request)
        self.assertEqual(resp.status_code,302,
                        "Should be redirected to new datagroup detail page")
        dg = DataGroup.objects.get(name='Walmart MSDS Test Group')
        self.assertIn(str(dg.pk), os.listdir(settings.MEDIA_ROOT))
        docs = DataDocument.objects.filter(data_group=dg)
        self.assertEqual(len(docs), 2)
        f = TemporaryUploadedFile(name='0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf',
                                content_type='application/pdf',
                                size=47,
                                charset=None)
        request = self.factory.post(path='/datagroup/%s' % dg.pk, data={'upload':'Submit'})
        request.FILES['multifiles'] = f
        request.user = User.objects.get(username='Karyn')
        resp = views.data_group_detail(request=request, pk=dg.pk)
        doc = DataDocument.objects.get(title='NUTRA NAIL')
        fn = doc.get_abstract_filename()
        folder_name = str(dg.pk)
        stored_file = f'{folder_name}/pdf/{fn}'
        self.assertTrue(os.path.exists(settings.MEDIA_ROOT + stored_file))
        f.close()

# import os
# import zipfile
#
# from dashboard.models import *
#
# groups = DataGroup.objects.all()
# for group in groups:
#     nm = group.dgurl()
#     os.remove(group.zip_file)
#     zf = zipfile.ZipFile(group.zip_file, 'a', zipfile.ZIP_DEFLATED)
#     docs = DataDocument.objects.filter(data_group=group)
#     loc = f'media/{nm}/pdf/'
#     for doc in docs:
#         afn = doc.get_abstract_filename()
#         os.rename(loc + doc.filename, loc + afn)
#         zf.write(loc + afn, afn)
#     zf.close()
