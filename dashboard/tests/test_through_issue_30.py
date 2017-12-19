from django.test import TestCase, RequestFactory
from dashboard.models import DataSource
from dashboard.models import SourceType
from dashboard.models import DataGroup
from django.contrib.auth.models import User
from django.utils import timezone
from .testing_utilities import populate_test_db
from selenium import webdriver
from django.conf import settings
import time

class BasicTestCase(TestCase):
    def test_getting_root(self):
        self.client.get('/')

class TestThroughIssue30(TestCase):
    def setUp(self):
        # Populate database
        populate_test_db()

<<<<<<< HEAD
        #resp = self.client.post('/login/', {'username': 'admin', 'password': 't0ps3cret'})

    def test_good_login(self):
        browser = webdriver.Chrome(executable_path=settings.CHROMEDRIVER_PATH)
        # Open the show page for the data group created in testing_utilities.py
        url = "http://127.0.0.1:8000/datagroup/1"
        browser.get(url)
        print('--------browser.title---------------')
        print(browser.title)
        print('username, email, and hashed password')
        print(User.objects.get(username='admin').username)
        print(User.objects.get(username='admin').email)
        print(User.objects.get(username='admin').password)

        # the test driver needs to log in first
        username = browser.find_element_by_xpath('//*[@id="id_username"]')
        password = browser.find_element_by_xpath('//*[@id="id_password"]')

        username.click()
        username.send_keys('admin')
        print('--------username field contents---------------')
        print(username.text)

        password.send_keys('t0ps3cret')
        print('--------password---------------')
        print(password.text)
        # keep the page open to mess around and try entering the values by hand
        time.sleep(30)
        # now it should redirect to the data group page
        button = browser.find_element_by_xpath("/html/body/div/form/button")
        print('--------button---------------')
        print(button.get_attribute('innerHTML'))
        button.click()
        print('--------browser.title---------------')
        print(browser.title)
        self.assertEquals('Factotum', browser.title)
        

    
    def test_data_group_matched_docs(self):
        'Confirm that the DataGroup with no matched documents returns zero for matched_docs'
        dg = DataGroup.objects.filter(name='Test DG 1')[:1].get()
        self.assertEquals(dg.matched_docs(), 0)

    def test_datagroup_edit(self):
        resp = self.client.post('/datagroup/edit/1', {'downloaded_at': '2017-12-12 10:10:10'})
        #print('--------RESPONSE CONTENT---------------')
        #print(resp.content)
        self.assertEqual(resp.status_code, 200)

=======
    def test_data_group_matched_docs(self):
        # Confirm that the DataGroup with no related documents returns zero for matched_docs
        dg = DataGroup.objects.get(pk=1)
        self.assertEquals(dg.matched_docs(), 0)

        # Confirm that the DataGroup WITH related documents returns greater than zero for matched_docs
        dg = DataGroup.objects.get(pk=2)
        self.assertGreater(dg.matched_docs(), 0)
>>>>>>> 1c097efc05f2b887a37be640c529b22063f576d3
