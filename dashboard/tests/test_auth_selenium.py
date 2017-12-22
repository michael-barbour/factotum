from django.test import LiveServerTestCase
from selenium import webdriver
from django.conf import settings
from django.contrib.auth.models import User
import time


class TestAuthInBrowser(LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Chrome(executable_path=settings.CHROMEDRIVER_PATH)
		self.browser.implicitly_wait(5)
		self.user = User.objects.create_user(username='Karyn', email='kats.karyn@epa.gov',
											 password='specialP@55word')

	def tearDown(self):
		self.browser.quit()

	def test_login(self):
		self.browser.get(self.live_server_url + '/login/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Please sign in', body.text)
		username_input = self.browser.find_element_by_name("username")
		username_input.send_keys('Karyn')
		password_input = self.browser.find_element_by_name("password")
		password_input.send_keys('specialP@55word')
		time.sleep(2)
		self.browser.find_element_by_class_name('btn').click()
		self.browser.get(self.live_server_url + '/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Welcome to Factotum', body.text)
		time.sleep(3)



