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

    # superfluous unit test
    def test_data_group_matched_docs(self):
        'Confirm that the DataGroup with no matched documents returns zero for matched_docs'
        dg = DataGroup.objects.filter(name='Test DG 1')[:1].get()
        self.assertEquals(dg.matched_docs(), 0)

        #resp = self.client.post('/login/', {'username': 'admin', 'password': 't0ps3cret'})

    def test_good_login(self):
        browser = webdriver.Chrome(executable_path=settings.CHROMEDRIVER_PATH)
        # Confirm that the `admin` user has been created
        print('username, email, and hashed password')
        print(User.objects.get(username='admin').username)
        print(User.objects.get(username='admin').email)
        print(User.objects.get(username='admin').password)
        # Open the show page for the data group created in testing_utilities.py
        url = "http://127.0.0.1:8000/login/?next=/"
        browser.get(url)
        print('--------browser.title---------------')
        print(browser.title) # This should be `login`
        self.assertEquals('admin', User.objects.get(username='admin').username)

        # the test driver needs to log in first

        # find and fill the username input box
        username = browser.find_element_by_xpath('//*[@id="id_username"]')
        username.click()
        username.send_keys('admin')
        print('--------username field contents---------------')
        print(username.text)

        # find and fill the password input box
        password = browser.find_element_by_xpath('//*[@id="id_password"]')
        password.send_keys('t0ps3cret')
        print('--------password---------------')
        print(password.text)

        # Click the "Sign In" button
        button = browser.find_element_by_xpath("/html/body/div/form/button")
        button.click()
        
        # keep the page open to mess around and try entering the values by hand
        time.sleep(20)
        # now it should redirect to the index page

        print('--------browser.title---------------')
        print(browser.title)
        self.assertEquals('Factotum', browser.title)
        
# The subsequent tests will not pass if the login has not worked
    def test_datagroup_edit(self):
        resp = self.client.post('/datagroup/edit/1', {'downloaded_at': '2017-12-12 10:10:10'})
        #print('--------RESPONSE CONTENT---------------')
        #print(resp.content)
        self.assertEqual(resp.status_code, 200)

