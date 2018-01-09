import unittest
from selenium import webdriver

URL = 'http://127.0.0.1:8000'

def log_karyn_in(object):
	'''
	Log user in for further testing.
	'''
	object.browser.get(URL + '/login/')
	body = object.browser.find_element_by_tag_name('body')
	object.assertIn('Please sign in', body.text)
	username_input = object.browser.find_element_by_name("username")
	username_input.send_keys('Karyn')
	password_input = object.browser.find_element_by_name("password")
	password_input.send_keys('specialP@55word')
	object.browser.find_element_by_class_name('btn').click()


class TestAuthInBrowser(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		log_karyn_in(self)

	def tearDown(self):
		self.browser.quit()

	def test_login(self):
		self.browser.get(URL + '/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Welcome to Factotum', body.text)

class TestDataSource(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		log_karyn_in(self)

	def tearDown(self):
		self.browser.quit()

	def test_data_source_name(self):
		self.browser.get(URL + '/datasource/1')
		h1 = self.browser.find_element_by_name('title')
		self.assertIn('Walmart MSDS', h1.text)

class TestDataGroup(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		log_karyn_in(self)

	def tearDown(self):
		self.browser.quit()

	def test_data_group_name(self):
		self.browser.get(URL + '/datagroup/1')
		h1 = self.browser.find_element_by_name('title')
		self.assertIn('Walmart MSDS', h1.text)
