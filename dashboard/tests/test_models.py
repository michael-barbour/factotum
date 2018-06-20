import csv
from django.utils import timezone
from django.test import TestCase

from dashboard.models import *
from .loader import load_model_objects

def create_data_documents(data_group, source_type, pdfs):
    '''Used to imitate the creation of new DataDocuments from CSV'''
    dds = []
    with open('./sample_files/register_records_matching.csv', 'r') as dg_csv:
        table = csv.DictReader(dg_csv)
        for line in table: # read every csv line, create docs for each
            if line['title'] == '': # updates title in line object
                line['title'] = line['filename'].split('.')[0]
            dd = DataDocument.objects.create(filename=line['filename'],
                                            title=line['title'],
                                            product_category=line['product'],
                                            url=line['url'],
                                            matched = line['filename'] in pdfs,
                                            data_group=data_group)
            dd.save()
            dds.append(dd)
        return dds

class ModelsTest(TestCase):

    def setUp(self):
        self.objects = load_model_objects()
        self.client.login(username='Karyn', password='specialP@55word')
        self.pdfs = ['0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf',
                        '0c68ab16-2065-4d9b-a8f2-e428eb192465.pdf']

    def test_object_creation(self):
        self.assertTrue(isinstance(self.objects.ds, DataSource))
        self.assertTrue(isinstance(self.objects.dg, DataGroup))
        self.assertTrue(isinstance(self.objects.script, Script))
        self.assertTrue(isinstance(self.objects.extext, ExtractedText))
        self.assertTrue(isinstance(self.objects.ec, ExtractedChemical))
        self.assertTrue(isinstance(self.objects.dsstox, DSSToxSubstance))
        self.assertTrue(isinstance(self.objects.ing, Ingredient))
        self.assertTrue(isinstance(self.objects.p, Product))
        self.assertTrue(isinstance(self.objects.pi, ProductToIngredient))
        self.assertTrue(isinstance(self.objects.pd, ProductDocument))
        self.assertTrue(isinstance(self.objects.dsi,
                                            DSSToxSubstanceToIngredient))
        self.assertTrue(isinstance(self.objects.pa, ProductAttribute))

    def test_object_properties(self):
        # Test properties of objects
        # DataSource
        self.assertEqual(self.objects.ds.__str__(), self.objects.ds.title)

        # DataGroup
        self.assertEqual(self.objects.dg.__str__(), self.objects.dg.name)
        self.assertEqual(self.objects.dg.dgurl(),
                            self.objects.dg.name.replace(' ', '_'))
        # DataDocuments
        # Confirm that one of the data documents appears in the data group
        # show page after upload from CSV
        docs = create_data_documents(self.objects.dg,self.objects.st, self.pdfs)
        self.assertEqual(len(docs),2, ('Only 2 records should be created!'))
        dg_response = self.client.get('/datagroup/' + str(self.objects.dg.pk))
        self.assertIn(b'NUTRA', dg_response.content)
        self.assertEqual(len(self.pdfs), 2)
        # Confirm that the two data documents in the csv file are matches to
        # the pdfs via their file names
        self.assertEqual(self.objects.dg.matched_docs(), 2)
        # Test a link to an uploaded pdf
        u = b'Data_Group_for_Test/pdf/0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf'
        self.assertIn(u, dg_response.content, (
                                    'link to PDF should be in HTML!'))
        # ExtractionScript
        self.assertEqual(self.objects.script.__str__(), 'Test Title')
        # ExtractedText
        self.assertEqual(self.objects.extext.__str__(),
                                    'Test Extracted Text Record')
        # ExtractedChemical
        self.assertEqual(self.objects.ec.__str__(), 'Test Chem Name')
        # DSSToxSubstance
        self.assertEqual(self.objects.dsstox.__str__(),
                                    self.objects.ec.__str__())

    def test_product_attribute(self):
        self.assertEqual(ProductToAttribute.objects.count(), 0)
        p2a = ProductToAttribute.objects.create(product=self.objects.p,
                                            product_attribute=self.objects.pa)
        self.assertEqual(ProductToAttribute.objects.count(), 1)
