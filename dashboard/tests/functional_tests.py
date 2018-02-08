import csv
import time
import unittest
import collections
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from django.conf import settings
from django.utils import timezone
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile

from dashboard.models import (DataGroup, DataSource, DataDocument,
                                Script, ExtractedText, Product)

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




class TestAuthInBrowser(LiveServerTestCase):

    fixtures = ['seed_data']

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        self.browser.get(self.live_server_url )
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Please sign in', body.text,
                        "Confirm that the login page is displayed")
        log_karyn_in(self)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Welcome to Factotum', body.text)

class TestDataSource(LiveServerTestCase):

    fixtures = ['seed_data']

    def setUp(self):
        self.browser = webdriver.Chrome()
        log_karyn_in(self)

    def tearDown(self):
        self.browser.quit()

    def test_data_source_name(self):
        self.browser.get(self.live_server_url + '/datasource/1')
        h1 = self.browser.find_element_by_name('title')
        self.assertIn('Walmart MSDS', h1.text)

    # When a new data source is entered, the data source is automatically
    # assigned the state 'awaiting triage.'
    def test_state_and_priority(self):
        valid_states = ['Awaiting Triage','In Progress','Complete','Stale']
        valid_priorities = ['High','Medium','Low']
        self.browser.get(self.live_server_url + '/datasource/1')
        state = self.browser.find_element_by_name('state')
        self.assertIn(state.text, valid_states)
        self.assertIn('Awaiting Triage', state.text)
        select = Select(self.browser.find_element_by_name('priority'))
        self.assertEqual([o.text for o in select.options], valid_priorities)
        selected_option = select.first_selected_option
        self.assertIn(selected_option.text, valid_priorities)
        # is there a better way to loop through datasources???
        # do we need to do all ????
        self.browser.get(self.live_server_url + '/datasource/2')
        state = self.browser.find_element_by_name('state')
        self.assertIn(state.text, valid_states)
        self.assertIn('Awaiting Triage', state.text)

    def test_datagroup_list_length(self):
        b = len(DataGroup.objects.filter(data_source_id=1))
        self.browser.get(self.live_server_url + '/datasource/1')
        row_count = len(self.browser.find_elements_by_xpath(
                                "//table[@id='groups']/tbody/tr"))
        self.assertEqual(b, row_count)


class TestDataGroup(LiveServerTestCase):

    fixtures = ['seed_data']

    def setUp(self):
        self.browser = webdriver.Chrome()
        log_karyn_in(self)

    def tearDown(self):
        self.browser.quit()

    def test_data_group_name(self):
        self.browser.get(self.live_server_url + '/datagroup/1')
        h1 = self.browser.find_element_by_name('title')
        self.assertIn('Walmart MSDS', h1.text)
        pdflink = self.browser.find_elements_by_xpath(
                                '/html/body/div/table/tbody/tr[1]/td[1]/a')[0]
        self.assertIn('shampoo.pdf',pdflink.get_attribute('href'))

    def create_data_group(self, data_source, testusername = 'Karyn',
                            name='Walmart MSDS 3',
                            description=('Another data group, '
                                         'added programatically')):
        source_csv = open('./sample_files/walmart_msds_3.csv','rb')
        return DataGroup.objects.create(name=name,
                description=description, data_source = data_source,
                downloaded_by=User.objects.get(username=testusername) ,
                downloaded_at=timezone.now(),
                csv=SimpleUploadedFile('walmart_msds_3.csv', source_csv.read()))

    def upload_pdfs(self):
        store = settings.MEDIA_URL + self.dg.dgurl()
        pdf1_name = '0ffeb4ae-2e36-4400-8cfc-a63611011d44.pdf'
        pdf2_name = '1af3fa0f-edf3-4a41-bcec-7436d0689bd8.pdf'
        local_pdf = open('./sample_files/' + pdf1_name, 'rb')
        fs = FileSystemStorage(store + '/pdf')
        fs.save(pdf1_name, local_pdf)
        local_pdf = open('./sample_files/' + pdf2_name, 'rb')
        fs = FileSystemStorage(store + '/pdf')
        fs.save(pdf2_name, local_pdf)
        return [pdf1_name, pdf2_name]

    def create_data_documents(self, data_group, data_source):
        dds = []
        #pdfs = [f for f in os.listdir('/media/' + self.dg.dgurl() + '/pdf') if f.endswith('.pdf')]
        #pdfs
        with open(data_group.csv.path) as dg_csv:
            table = csv.DictReader(dg_csv)
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
                        data_group=data_group,
                        data_source=data_source)
                    dds.append(dd)
            return dds

    # creation of another DataGroup from csv and pdf sources
    def test_new_data_group(self):
        # DataGroup, created using the model layer
        dg_count_before = DataGroup.objects.count()
        ds = DataSource.objects.get(pk=1)
        self.dg = self.create_data_group(data_source=ds)
        dg_count_after = DataGroup.objects.count()
        self.assertEqual(dg_count_after, dg_count_before + 1,
                            "Confirm the DataGroup object has been created")
        self.assertEqual(3, self.dg.pk,
                            "Confirm the new DataGroup object's pk is 3")
        self.pdfs = self.upload_pdfs()
        self.dds = self.create_data_documents(self.dg, ds)

        # Use the browser layer to confirm that the object has been created
        self.browser.get('%s%s' % (self.live_server_url, '/datagroup/3'))
        self.assertEqual('factotum', self.browser.title,
                            "Testing open of datagroup 3 show page")

        self.browser.get(self.live_server_url + reverse('data_group_detail',
                                                    kwargs={'pk': self.dg.pk}))
        self.assertEqual('factotum', self.browser.title)
        h1 = self.browser.find_element_by_name('title')
        self.assertEqual('Walmart MSDS 3', h1.text)

        # Use the browser layer to delete the DataGroup object
        # deleting the DataGroup should clean up the file system
        self.browser.get(self.live_server_url + '/datagroup/delete/3')
        del_button = self.browser.find_elements_by_xpath(('/html/body/div/form/'
                                                                'input[2]'))[0]
        del_button.click()
        self.assertEqual(DataGroup.objects.count(), dg_count_before ,
                            "Confirm the DataGroup object has been deleted")

class TestProductCuration(LiveServerTestCase):

    fixtures = ['seed_data']

    def setUp(self):
        self.browser = webdriver.Chrome()
        log_karyn_in(self)

    def tearDown(self):
        self.browser.quit()

    def test_unlinked_documents(self):
        self.browser.get(self.live_server_url + '/product_curation/')
        src_title = self.browser.find_elements_by_xpath(
                                '/html/body/div/table/tbody/tr[1]/td[1]/a')[0]
        ds = DataSource.objects.get(title=src_title.text)
        un_link = self.browser.find_elements_by_xpath(
                                '/html/body/div/table/tbody/tr[1]/td[3]/a')[0]
        self.assertEqual(un_link.get_attribute("href").split('/')[-1],
                                                                    str(ds.pk))

    def test_PUC_assignment(self):
        self.browser.get(self.live_server_url + '/product_curation/')
        src_title = self.browser.find_elements_by_xpath(
                                '/html/body/div/table/tbody/tr[1]/td[1]/a')[0]
        ds = DataSource.objects.get(title=src_title.text)
        puc_link = self.browser.find_elements_by_xpath(
                                '/html/body/div/table/tbody/tr[1]/td[4]/a')[0]
        products_missing_PUC = str(len(ds.source.filter(prod_cat__isnull=True)))
        self.assertEqual(puc_link.text, products_missing_PUC, ('The Assign PUC '
                            'link should display # of Products without a PUC'))

class TestQAScoreboard(LiveServerTestCase):
    # Issue 35 https://github.com/HumanExposure/factotum/issues/35
    # Definition of Done:
    # A QA Home Page
    # A link in the nav bar to the QA Home page
    # A Table on the QA Home page
    # A button for each row in the table that will take you to #36 (Not Implemented Yet)
    fixtures = ['seed_data']

    def setUp(self):
        self.browser = webdriver.Chrome()
        log_karyn_in(self)

    def tearDown(self):
        self.browser.quit()

    def test_scoreboard(self):

        # A link in the nav bar to the QA Home page
        self.browser.get('%s%s' % (self.live_server_url, ''))
        nav_html = self.browser.find_element_by_xpath('//*[@id="navbarCollapse"]/ul').get_attribute('innerHTML')
        self.assertIn('href="/qa/"', nav_html,
        'The link to /qa/ must be in the nav list')

        self.browser.get('%s%s' % (self.live_server_url, '/qa'))
        scriptcount = Script.objects.filter(script_type='EX').count()

        # A Table on the QA home page
        row_count = len(self.browser.find_elements_by_xpath(
            "//table[@id='extraction_script_table']/tbody/tr"))
        self.assertEqual(scriptcount, row_count, ('The seed data contains one '
                    'ExtractionScript object that should appear in this table'))

        displayed_doc_count = self.browser.find_elements_by_xpath(
            '//*[@id="extraction_script_table"]/tbody/tr/td[2]')[0].text
        model_doc_count = DataDocument.objects.filter(
                                    extractedtext__extraction_script=1).count()
        self.assertEqual(displayed_doc_count, str(model_doc_count),
                        ('The displayed number of datadocuments should match '
                        'the number of data documents whose related extracted '
                        'text objects used the extraction script'))

        displayed_pct_checked = self.browser.find_elements_by_xpath(
            '//*[@id="extraction_script_table"]/tbody/tr/td[3]')[0].text
        #this assumes that pk=1 will be a script_type of 'EX'
        model_pct_checked = Script.objects.get(pk=1).get_pct_checked()
        self.assertEqual(displayed_pct_checked, model_pct_checked,
                        ('The displayed percentage should match what is '
                        'derived from the model'))

        es = Script.objects.get(pk=1)
        self.assertEqual(es.get_qa_complete_extractedtext_count(), 0,
                        ('The ExtractionScript object should return 0'
                        'qa_checked ExtractedText objects'))
        self.assertEqual(model_pct_checked, '0%')
        # Set qa_checked property to True for one of the ExtractedText objects
        self.assertEqual(ExtractedText.objects.get(pk=1).qa_checked , False)
        et_change = ExtractedText.objects.get(pk=1)
        et_change.qa_checked = True
        et_change.save()
        self.assertEqual(ExtractedText.objects.get(pk=1).qa_checked , True,
                        'The object should now have qa_checked = True')

        es = Script.objects.get(pk=1)
        self.assertEqual(es.get_qa_complete_extractedtext_count(), 1,
                        ('The ExtractionScript object should return 1 '
                        'qa_checked ExtractedText object'))

        self.assertEqual(1, es.get_qa_complete_extractedtext_count(),
                        'Check the numerator in the model layer')
        self.assertEqual(2, es.get_datadocument_count(),
                        'Check the denominator in the model layer')
        model_pct_checked = Script.objects.get(pk=1).get_pct_checked()
        self.assertEqual(model_pct_checked, '50%',
                        ('The get_pct_checked() method should return 50 pct'
                        ' from the model layer'))
        self.browser.refresh()

        displayed_pct_checked = self.browser.find_elements_by_xpath(
            '//*[@id="extraction_script_table"]/tbody/tr/td[3]')[0].text

        self.assertEqual(displayed_pct_checked, model_pct_checked,
                        ('The displayed percentage in the browser layer should '
                        'reflect the newly checked extracted text object'))
        # A button for each row that will take you to the script's QA page
        # https://github.com/HumanExposure/factotum/issues/36
        script_qa_link = self.browser.find_element_by_xpath(
            '//*[@id="extraction_script_table"]/tbody/tr/td[4]/a'
        )
        # Before clicking the link, the script's qa_done property
        # should be false
        self.assertEqual(Script.objects.get(pk=1).qa_begun, False,
        'The qa_done property of the Script should be False')

        script_qa_link.click()
        # The link should open a page where the h1 text matches the title
        # of the Script
        h1 = self.browser.find_element_by_xpath('/html/body/div/h1').text
        self.assertIn(Script.objects.get(pk=1).title, h1,
        'The <h1> text should equal the .title of the Script')

        # Opening the ExtractionScript's QA page should set its qa_begun
        # property to True
        self.assertEqual(Script.objects.get(pk=1).qa_begun, True,
        'The qa_done property of the ExtractionScript should now be True')
        # Go back to the QA index page to confirm
        self.browser.get('%s%s' % (self.live_server_url, '/qa'))
        script_qa_link = self.browser.find_element_by_xpath(
            '//*[@id="extraction_script_table"]/tbody/tr/td[4]/a'
        )
        self.assertEqual(script_qa_link.text, 'Continue QA',
        'The QA button should now say "Continue QA" instead of "Begin QA"')



def clean_label(self, label):
    """Remove the "remove" character used in select2."""
    return label.replace('\xd7', '')


def wait_for_element(self, elm, by = 'id', timeout=10):
    wait = WebDriverWait(self.browser, timeout)
    wait.until(EC.presence_of_element_located((By.XPATH, elm)))
    return self.browser.find_element_by_xpath(elm)


class TestPUCAssignment(LiveServerTestCase):
    # Issue 80 https://github.com/HumanExposure/factotum/issues/80
    #
    fixtures = ['seed_data','seed_product_category.yaml']

    def setUp(self):
        self.browser = webdriver.Chrome()
        log_karyn_in(self)

    def tearDown(self):
        self.browser.quit()

    def test_puc(self):

        # As Karyn the Curator
        # I want the ability to assign product categories (PUCs) to a product
        # So that I can more easily navigate through products if they are grouped.

        # From the assignment of product category
        # Click button, form appears which shows you a pdf icon allowing you to view pdf,
        # product name (Product.title), auto complete box for PUC - when you start typing
        # auto complete looks at general, specific, product family to match what the user
        # is typing (auto complete should work like Google), expect minimum of three
        # characters before auto complete appears
        self.browser.get('%s%s' % (self.live_server_url, '/product_puc/1'))
        h2 = self.browser.find_element_by_xpath('/html/body/div/h2').text
        self.assertIn(Product.objects.get(pk=1).title, h2,
        'The <h2> text should equal the .title of the product')

        puc_before = Product.objects.get(pk=1).prod_cat

        puc_selector = self.browser.find_element_by_xpath('//*[@id="id_prod_cat"]')
        puc_selector = self.browser.find_element_by_xpath('//*[@id="select2-id_prod_cat-container"]')
        puc_sibling = self.browser.find_element_by_xpath('//*[@id="id_prod_cat"]/following::*')
        puc_sibling.click()

        #wait_for_element(self, "select2-search__field", "class").click()
        puc_input = self.browser.find_element_by_class_name('select2-search__field')
        puc_input.send_keys('pet care')

        # The driver cannot immediately type into the input box - it needs
        # to load an element first, as explained here:
        # https://stackoverflow.com/questions/34422274/django-selecting-autocomplete-light-choices-with-selenium

        wait_for_element(self,
            '//*[@id="select2-id_prod_cat-results"]/li[2]',
            "xpath").click()
        puc_selector = self.browser.find_element_by_xpath('//*[@id="select2-id_prod_cat-container"]')
        self.assertEqual(puc_selector.text, 'Pet care - all pets -')

        submit_button = self.browser.find_element_by_xpath('/html/body/div/div/form/button')
        submit_button.click()
        puc_after = Product.objects.get(pk=1).prod_cat
        # check the model layer for the change
        self.assertNotEqual(puc_before, puc_after, "The object's prod_cat should have changed")
