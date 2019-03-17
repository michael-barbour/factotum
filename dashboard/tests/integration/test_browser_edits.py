from lxml import html

from django.test import TestCase
from dashboard.tests.loader import load_model_objects, fixtures_standard
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from dashboard.models import *
from selenium import webdriver
from django.conf import settings
from selenium.webdriver.support.select import Select


def log_karyn_in(object):
    '''
    Log user in for further testing.
    '''
    object.browser.get(object.live_server_url + '/login/')
    body = object.browser.find_element_by_tag_name('body')
    object.assertIn('Please sign in', body.text)
    username_input = object.browser.find_element_by_name("username")
    username_input.send_keys('Karyn')
    password_input = object.browser.find_element_by_name("password")
    password_input.send_keys('specialP@55word')
    object.browser.find_element_by_class_name('btn').click()


class TestEditsWithSeedData(StaticLiveServerTestCase):
    fixtures = fixtures_standard

    def setUp(self):
        if settings.TEST_BROWSER == 'firefox':
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Chrome()
        log_karyn_in(self)

    def tearDown(self):
        self.browser.quit()

    def test_break_curation(self):
        '''
        Changing the raw_cas or raw_chemname on a RawChem record with a related DssToxLookup should cause
        the relationship to be deleted.
        '''
        # currently uses a single data document
        ets_with_curation = ExtractedText.objects.filter(
            rawchem__dsstox__isnull=False).filter(pk=245401)
        for et in ets_with_curation:
            doc_qa_link = f'/qa/extractedtext/%s/' % et.data_document_id
            self.browser.get(self.live_server_url + doc_qa_link)

            rc_id = self.browser.find_element_by_xpath(
                '//*[@id="id_rawchem-0-rawchem_ptr"]').get_attribute('value')
            true_cas = self.browser.find_element_by_xpath(
                '//*[@id="id_rawchem-0-true_cas"]').get_attribute('value')
            rc = RawChem.objects.get(pk=rc_id)
            self.assertEqual(true_cas, rc.dsstox.true_cas,
                             'The displayed True CAS should match the object attribute')
            self.browser.find_element_by_xpath(
                '//*[@id="btn-toggle-edit"]').click()
            raw_cas_input = self.browser.find_element_by_xpath(
                '//*[@id="id_rawchem-0-raw_cas"]')
            raw_cas_input.send_keys('changed cas')
            self.browser.find_element_by_xpath('//*[@id="save"]').click()
            rc = RawChem.objects.get(pk=rc_id)   # reload the rawchem record
            self.assertEqual(
                None, rc.dsstox, 'The same rawchem record should now have nothing in its dsstox link')

    def test_new_chem(self):
        '''
        Adding a new ExtractedChemical without a unity type should return a validation error
        '''
        # currently "loops" over just a single data document. Other cases can be added
        ets_with_curation = ExtractedText.objects.filter(
            rawchem__dsstox__isnull=False).filter(pk=245401)
        for et in ets_with_curation:
            doc_qa_link = f'/qa/extractedtext/%s/' % et.data_document_id
            self.browser.get(self.live_server_url + doc_qa_link)

            self.browser.find_element_by_xpath(
                '//*[@id="btn-toggle-edit"]').click()
            raw_cas_input = self.browser.find_element_by_xpath(
                '//*[@id="id_rawchem-1-raw_cas"]')
            raw_cas_input.send_keys('test raw cas')
            self.browser.find_element_by_xpath('//*[@id="save"]').click()
            # Check for the error message after clicking Save
            parent_div = self.browser.find_element_by_xpath(
                '//*[@id="id_rawchem-1-raw_cas"]/parent::*')
            card_div = parent_div.find_element_by_xpath(
                '../..')
            self.assertTrue("errorlist" in card_div.get_attribute("innerHTML"))

            # Try editing a new record correctly
            self.browser.find_element_by_xpath(
                '//*[@id="btn-toggle-edit"]').click()
            raw_cas_input = self.browser.find_element_by_xpath(
                '//*[@id="id_rawchem-1-raw_cas"]')
            raw_cas_input.send_keys('test raw cas')
            # The unit_type field is the only required one
            unit_type_select = Select(self.browser.find_element_by_xpath(
                '//*[@id="id_rawchem-1-unit_type"]'))
            unit_type_select.select_by_index(1)

            self.browser.find_element_by_xpath('//*[@id="save"]').click()
            # Check for the absence of an error message after clicking Save
            parent_div = self.browser.find_element_by_xpath(
                '//*[@id="id_rawchem-1-raw_cas"]/parent::*')
            card_div = parent_div.find_element_by_xpath(
                '../..')
            self.assertFalse(
                "errorlist" in card_div.get_attribute("innerHTML"))

    def test_listpresence_qa(self):
        '''
        The QA Chemical Presence index page should show a link for each ExtractedCPCat
        record. Clicking one of those links for the first time runs the
        prep_cp_for_qa() method. The method sets the qa_flag attribute for randomly
        chosen ExtractedListPresence records
        '''
        # Start at the list of data groups
        qa_index_link = '/qa/chemicalpresence' 
        self.browser.get(self.live_server_url + qa_index_link)
        dg_link = self.browser.find_element_by_xpath(
            '//*[@id="chemical_presence_table"]/tbody/tr[2]/td[4]/a')
        dg_url = dg_link.get_attribute("href").rstrip("/")
        dg_id = dg_url.split("/")[-1]
        dg = DataGroup.objects.get(pk=dg_id)
        # Count the qa_flag records inside the data group's data documents
        dds = dg.datadocument_set.select_related('extractedtext__extractedcpcat').filter(extractedtext__extractedcpcat__isnull=False)
        for dd in dds:
            qa_count = dd.extractedtext.extractedcpcat.rawchem.select_subclasses().filter(extractedlistpresence__qa_flag=True).count()
            self.assertEqual(qa_count, 0, 'There should be no QA-flagged child records under any ExtractedListPresence')

        # click through to the second datagroup with extracted CPCat records
        # this causes the prep_cp_for_qa method to run
        dg_link.click()

        # Get the ExtractedCPCat record that corresponds to the second row
        cpcat_link = self.browser.find_element_by_xpath(
            '//*[@id="extracted_text_table"]/tbody/tr[2]/td[4]/a')
        cpcat_url = cpcat_link.get_attribute("href").rstrip("/")
        cpcat_id = cpcat_url.split("/")[-1]
        
        cpcat = ExtractedCPCat.objects.get(pk=cpcat_id)
        elps = cpcat.rawchem.select_subclasses()
        qa_elp_count = elps.filter(extractedlistpresence__qa_flag=True).count()
        self.assertTrue(qa_elp_count > 0, 'After clicking the link there should be some qa_flag records')
        
