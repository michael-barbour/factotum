from dashboard.tests.loader import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from dashboard.models import *
from django.urls import reverse

from selenium.webdriver.common.keys import Keys

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
        self.browser = load_browser()
        log_karyn_in(self)

    def tearDown(self):
        self.browser.quit()

    def test_list_presence_keywords(self):
        # testing Select2 functionality
        doc = DataDocument.objects.get(pk=254781)
        response = self.browser.get(self.live_server_url + reverse('data_document', kwargs={'pk': doc.pk}))
        # If Select2 widget is firing, we should start with 2 tags for this document
        dropdown = self.browser.find_element_by_xpath('//*[@id="id_tags"][count(option) = 2]')
        self.assertTrue(dropdown,
                        'Listpresence records for this doc should begin with 2 associated keywords')
        input = self.browser.find_element_by_xpath('//*[@id="id_tags"]/following-sibling::span[1]/descendant::input[1]')
        input.send_keys('pesticide' + Keys.ENTER)
        # input.send_keys()
        # dropdown = self.browser.find_element_by_xpath('//*[@id="id_tags"][count(option) = 3]')
        # self.assertTrue(dropdown,
        #                 'Listpresence records for this doc should now have 3 associated keywords')
        button = self.browser.find_element_by_xpath('//*[@id="id_tags"]/following-sibling::button[1]')
        button.click()


    def test_datadoc_add_extracted(self):
        '''
        Test that when a datadocument has no ExtractedText,
        the user can add one in the browser
        1.
        '''

        for doc_id in [155324   # CO record with no ExtractedText
                       ]:
            # QA Page
            dd_url = self.live_server_url + f'/datadocument/{doc_id}/'
            self.browser.get(dd_url)
            # Activate the edit mode
            self.browser.find_element_by_xpath(
                '//*[@id="btn-add-or-edit-extracted-text"]').click()

            # Verify that the modal window appears by finding the Cancel button
            # The modal window does not immediately appear, so the browser
            # should wait for the button to be clickable
            wait = WebDriverWait(self.browser, 10)
            cancel_button = wait.until(
                ec.element_to_be_clickable(
                    (By.XPATH, "//*[@id='extracted-text-modal-cancel']")
                )
            )
            self.assertEqual("Cancel", cancel_button.text,
                             'The Cancel button should say Cancel')
            cancel_button.click()
            # Verify that no ExtractedText record was created
            self.assertEqual(0, ExtractedText.objects.filter(
                data_document_id=doc_id).count(),
                "the count of ExtractedText records related to the \
                data document should be zero")

            # Wait for the modal div to disappear
            edit_modal = wait.until(
                ec.invisibility_of_element(
                    (By.XPATH, '//*[@id="extextModal"]')
                )
            )
            # Click the Add button again to reopen the editor
            add_button = self.browser.find_element_by_xpath(
                '//*[@id="btn-add-or-edit-extracted-text"]')
            add_button.click()
            # Once again, check that the controls on the modal form are clickable
            # before trying to interact with them
            cancel_button = wait.until(
                ec.element_to_be_clickable(
                    (By.XPATH, "//*[@id='extracted-text-modal-cancel']")
                )
            )
            prod_name_box = self.browser.find_element_by_id(
                'id_prod_name')
            # Add a prod_name value to the box
            prod_name_box.send_keys('Fake Product')
            save_button = self.browser.find_element_by_id(
                'extracted-text-modal-save')
            save_button.click()
            # Confirm the presence of the new ExtractedText record
            et = ExtractedText.objects.get(data_document_id=doc_id)
            self.assertEqual('Fake Product', et.prod_name,
                             "The prod_name of the new object should match what was entered")


