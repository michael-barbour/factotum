from django.test import TestCase, override_settings
from django.test import Client

from dashboard.tests.loader import *
from dashboard.views.data_document import *
from lxml import html


@override_settings(ALLOWED_HOSTS=['testserver'])
class DataDocumentDetailTest(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.client.login(username='Karyn', password='specialP@55word')

    def test_extractedtext_update(self):
        self.assertTrue(ExtractedTextForm().fields['prod_name'],
                        'ExtractedTextForm must include prod_name')
        dd = DataDocument.objects.get(pk=7)
        et = ExtractedText.objects.filter(data_document=dd).get()
        response = self.client.post(f'/datadocument/{dd.pk}/',
                                    {'prod_name': 'zzz',
                                     'rev_num': '1',
                                     'doc_date': '01/01/2018',
                                     'save_extracted_text': ''})
        et.refresh_from_db()
        self.assertEqual(et.prod_name, 'zzz',
                         'The ExtractedText for DataDocument 7 should have a prod_name of "zzz"')

    def test_documenttype_update(self):
        self.assertTrue(DocumentTypeForm().fields['document_type'],
                        'DocumentTypeForm must include document_type')
        dd = DataDocument.objects.get(pk=7)
        response = self.client.post(f'/datadocument/{dd.pk}/',
                                    {'document_type': 2})
        dd.refresh_from_db()
        self.assertEqual(dd.document_type_id, 2,
                         'DataDocument 7 should have a final document_type_id of 2')     

class TestDynamicDetail(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.c = Client()
        self.c.login(username='Karyn', password='specialP@55word')
    
    def test_fetch_extracted_records(self):
        ''' Confirm that each detail child object returned by the function has the correct parent '''
        for et in ExtractedText.objects.all():
            #print('Fetching extracted child records from %s: %s ' % (et.pk , et))
            for ex_child in et.fetch_extracted_records():
                child_model = ex_child.__class__ # the fetch_extracted_records function returns different classes
                #print('    %s: %s' % (ex_child.__class__.__name__ , ex_child ))
                self.assertEqual(et.pk , child_model.objects.get(pk=ex_child.pk).extracted_text.pk,
                    'The ExtractedChemical object with the returned child pk should have the correct extracted_text parent')


    def test_every_extractedtext(self):
        ''''Loop through all the ExtractedText objects and confirm that the new
        create_detail_formset method returns form values that match what the old  
        method delivered
        '''
        for et in ExtractedText.objects.all():
            # print('Testing formset creation for ExtractedText object %s (%s) ' % (et.pk, et ) )
            test_formset = create_detail_formset(et)
            # compare to the old method
            if (DataDocument.objects.get(id=et.data_document_id).data_group.group_type.code == 'HP'):
                old_fs = HnPFormSet(instance=et, prefix='detail')
                self.assertEqual(old_fs[0]['product_surveyed'].value(), 
                    test_formset[0]['product_surveyed'].value(),
                    'The old and new methods should return the same items')
            
            if (DataDocument.objects.get(id=et.data_document_id).data_group.group_type.code == 'CO'):
                old_fs = ChemicalFormSet(instance=et, prefix='detail')
                self.assertEqual(old_fs[0]['raw_chem_name'].value(), 
                    test_formset[0]['raw_chem_name'].value(),
                    'The old and new methods should return the same items')
            
            if (DataDocument.objects.get(id=et.data_document_id).data_group.group_type.code == 'CP'):
                # for Chemical Presence, there is no old form-construction method to compare to
                self.assertTrue(len(test_formset[0]['raw_chem_name'].value()) > 0, 
                    'There should be a raw_chem_name value')


        print('print(some important stuff)')
        print('|￣￣￣￣￣|')
        print('|   HI      |')
        print('|           |' )
        print('|  RICK     |' )    
        print('|           |')
        print('|___________|') 
        print('(\__/) || ')
        print('(•ㅅ•) || ')
        print('/ 　 づ')