from django.test import TestCase
from .loader import load_model_objects
from dashboard.models import DataGroup
from dashboard.views.data_group import ExtractionScriptForm, DataGroupForm
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import Client
from importlib import import_module


class DataGroupTest(TestCase):

    def setUp(self):
        self.objects = load_model_objects()
        self.client.login(username='Karyn', password='specialP@55word')

    def test_detail_form_load(self):
        pk = DataGroup.objects.first().pk
        response = self.client.get(f'/datagroup/{pk}')
        self.assertFalse(self.objects.doc.matched,
                    ('Document should start w/ matched False'))
        self.assertFalse(self.objects.doc.extracted,
                    ('Document should start w/ extracted False'))
        self.assertTrue(response.context['upload_form'],
                    ('UploadForm should be included in the page!'))
        self.assertFalse(response.context['extract_form'],
                    ('ExtractForm should not be included in the page!'))
        self.objects.doc.matched = True
        self.objects.doc.save()
        response = self.client.get(f'/datagroup/{pk}')
        self.assertFalse(response.context['upload_form'], (
                    'UploadForm should not be included in the page!'))
        self.assertIsInstance(response.context['extract_form'], ExtractionScriptForm,
                    ('ExtractForm should be included in the page!'))
        self.objects.doc.extracted = True
        self.objects.doc.save()
        response = self.client.get(f'/datagroup/{pk}')
        self.assertFalse(response.context['upload_form'],
                    ('UploadForm should not be included in the page!'))
        self.assertFalse(response.context['extract_form'],
                    ('ExtractForm should not be included in the page!'))

    def test_detail_template_fieldnames(self):
        pk = DataGroup.objects.first().pk
        self.assertEqual(str(self.objects.dg.group_type),'composition',
        'Type of DataGroup needs to be "composition" for this test.')
        response = self.client.get(f'/datagroup/{pk}')
        self.assertEqual(response.context['extract_fields'],
                ['data_document_id','data_document_filename', 'record_type',
                'prod_name','doc_date','rev_num', 'raw_cas', 'raw_chem_name',
                'report_funcuse','raw_min_comp','raw_max_comp', 'unit_type',
                'ingredient_rank', 'raw_central_comp'],
                "Fieldnames passed are incorrect!")
        self.objects.gt.title = 'functional_use'
        self.objects.gt.save()
        self.assertEqual(str(self.objects.dg.group_type),'functional_use',
        'Type of DataGroup needs to be "functional_use" for this test.')
        response = self.client.get(f'/datagroup/{pk}')
        self.assertEqual(response.context['extract_fields'],
                ['data_document_id','data_document_filename', 'record_type',
                'prod_name','doc_date','rev_num', 'raw_cas', 'raw_chem_name',
                'report_funcuse'],
                "Fieldnames passed are incorrect!")
    # def test_upload_errors(self):
    #     # pk = DataGroup.objects.first().pk
    #     # self.objects.doc.filename = 'test_filename.pdf'
    #     # content = b'datagroup,name,hair'
    #     # f = SimpleUploadedFile("file.pdf", content)
    #     # d = {'script_selection': ['5'],
    #     # 'weight_fraction_type': ['2'],
    #     # 'extract_form': [ExtractionScriptForm([f])],
    #     # 'extract_button': ['Submit']}
    #     title = 'Testicles'
    #     initial_values = {'downloaded_by' : self.objects.user,
    #                       'name'          : 'Testicles',
    #                       'data_source'   : self.objects.ds}
    #     form = DataGroupForm(
    #                          user    = self.objects.user,
    #                          initial = initial_values)
    #     # with open('./sample_files/register_records_missing_filename.csv') as fp:
    #     with open('./sample_files/register_records_matching.csv') as fp:
    #         response = self.client.post(f'/datagroup/new', { 'session' : {
    #                                                         'datasource_title': title},
    #                                                         # 'form': form,
    #                                                         'attachment': form})
    #
    #     print(response.content)


    # def test_extract_errors(self):
    #     pk = DataGroup.objects.first().pk
    #     self.objects.doc.filename = 'test_filename.pdf'
    #     with open('./sample_files/extract_test.csv') as fp:
    #         response = self.client.post(f'/datagroup/{pk}', {'upload':[],
    #         'attachment': fp})
    #         print(response.content)
        # content = b'datagroup,name,hair'
        # f = SimpleUploadedFile("file.pdf", content)
        # d = {'script_selection': ['5'],
        # 'weight_fraction_type': ['2'],
        # 'extract_form': [ExtractionScriptForm([f])],
        # 'extract_button': ['Submit']}




        # d = {'multifiles': [f]}

        # response = self.client.post(f'/datagroup/{pk}', d)
        # print(self.objects.doc.filename)
        # print(response.context['all_documents'])

# <!-- request.POST -->
# <QueryDict: {'csrfmiddlewaretoken': ['hhkUa1TcXA8sOtgcUjPEQRe5MnEIILEh4EVp5P4E3P3YIJiAsPWKaw6qKd41SldU'],
# 'script_selection': ['5'],
# 'weight_fraction_type': ['1'],
# 'extract_button': ['Submit']}>
#
# <!-- request.FILES -->
# <MultiValueDict: {'extract_file': [<InMemoryUploadedFile: extracted_text_invalid_choices.csv (text/csv)>]}>

# content = b'datagroup,name,hair'
# f = SimpleUploadedFile("file.txt", content)
# response = self.client.post(f'/datagroup/{pk}',
#                         {'attachment':f, 'extract_button': ['Submit']})

# fieldnames = ['data_document_pk','data_document_filename',
#                       'record_type','prod_name','doc_date','rev_num',
#                       'raw_cas', 'raw_chem_name','raw_min_comp',
#                       'raw_max_comp', 'units', 'report_funcuse',
#                       'ingredient_rank', 'raw_central_comp']

# <MultiValueDict: {'multifiles': [<TemporaryUploadedFile: test_extract.csv (text/csv)>,
# <TemporaryUploadedFile: raid_msds.pdf (application/pdf)>, <TemporaryUploadedFile: 1af3fa0f-edf3-4a41-bcec-7436d0689bd8.pdf (application/pdf)>, <TemporaryUploadedFile: 7768cebf-3b87-4c87-9998-9a48b7c6eb18.pdf (application/pdf)>, <TemporaryUploadedFile: walmart_msds_3.csv (text/csv)>, <TemporaryUploadedFile: 0fa41af6-21e6-48ab-8053-ed4309e7a21e.pdf (application/pdf)>, <TemporaryUploadedFile: adams_flea_tick_shampoo.pdf (application/pdf)>, <TemporaryUploadedFile: 0c68ab16-2065-4d9b-a8f2-e428eb192465.pdf (application/pdf)>, <TemporaryUploadedFile: register_records_matching.csv (text/csv)>, <TemporaryUploadedFile: 3db7e2d6-af22-4d5d-9781-3f0fb6e23769.pdf (application/pdf)>, <TemporaryUploadedFile: .~lock.extracted_text_invalid_choices.csv# (application/octet-stream)>, <TemporaryUploadedFile: register_records_DG2.csv (text/csv)>, <TemporaryUploadedFile: 3490d9be-126f-4710-bac2-b78c7d6dbe2c.pdf (application/pdf)>, <TemporaryUploadedFile: revisedPUCs_2017_12_14.xls (application/vnd.ms-excel)>, <TemporaryUploadedFile: 08905c83-8446-4a35-9aa1-24a1186d42b9.pdf (application/pdf)>, <TemporaryUploadedFile: extracted_text_invalid_choices.csv (text/csv)>, <TemporaryUploadedFile: raid_ant_killer.pdf (application/pdf)>, <TemporaryUploadedFile: register_records_missing_title.csv (text/csv)>, <TemporaryUploadedFile: register_records_DG1.csv (text/csv)>, <TemporaryUploadedFile: 27d2eae7-d168-4b7b-b49c-240f43c8e194.pdf (application/pdf)>, <TemporaryUploadedFile: register_records_missing_filename.csv (text/csv)>, <TemporaryUploadedFile: 0c74b5ce-ec6e-47b9-87aa-c896da06081e.pdf (application/pdf)>, <TemporaryUploadedFile: 1b2adf0f-8a22-4d8d-bacc-b910fa1bdcc7.pdf (application/pdf)>, <TemporaryUploadedFile: 01f87329-83dd-4f54-9c12-bf423a6feada.pdf (application/pdf)>, <TemporaryUploadedFile: test_extract_good.csv (text/csv)>, <TemporaryUploadedFile: 0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf (application/pdf)>, <TemporaryUploadedFile: extracted_text_matching.csv (text/csv)>, <TemporaryUploadedFile: 33a754f1-8050-4470-b687-14b23c4f3cfc.pdf (application/pdf)>, <TemporaryUploadedFile: 39c2ed91-8782-40f3-886e-26848ad7d8b9.pdf (application/pdf)>, <TemporaryUploadedFile: 467cf595-ea28-4af9-8125-f31fa380328d.pdf (application/pdf)>, <TemporaryUploadedFile: 0ffeb4ae-2e36-4400-8cfc-a63611011d44.pdf (application/pdf)>, <TemporaryUploadedFile: 9ab2d0b4-1b5b-4595-b477-84bc4321d194.pdf (application/pdf)>, <TemporaryUploadedFile: e0719b3d-8387-498a-bbc3-ff2f9307b318.pdf (application/pdf)>, <TemporaryUploadedFile: register_test_search.csv (text/csv)>, <TemporaryUploadedFile: 0d8f0a7f-3afe-4766-b275-bcf2f0c0de10.pdf (application/pdf)>, <TemporaryUploadedFile: 8cb4befd-e659-42b7-bf2f-294146c828f5.pdf (application/pdf)>]}>
