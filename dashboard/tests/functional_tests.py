import unittest
from selenium import webdriver
from selenium.webdriver.support.select import Select

from django.test import LiveServerTestCase

from dashboard.models import DataGroup

# val = len(DataGroup.objects.filter(data_source_id=1))
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

class TestDataSource(LiveServerTestCase):

	fixtures = ['seed_data']

	def setUp(self):
		self.browser = webdriver.Chrome()
		log_karyn_in(self)

	def tearDown(self):
		self.browser.quit()

	def test_data_source_name(self):
		self.browser.get(URL + '/datasource/1')
		h1 = self.browser.find_element_by_name('title')
		self.assertIn('Walmart MSDS', h1.text)

	#When a new data source is entered, the data source is automatically assigned the state 'awaiting triage.'
	def test_state_and_priority(self):
		valid_states = ['Awaiting Triage','In Progress','Complete','Stale']
		valid_priorities = ['High','Medium','Low']
		self.browser.get(URL + '/datasource/1')
		state = self.browser.find_element_by_name('state')
		self.assertIn(state.text, valid_states)
		self.assertIn('Awaiting Triage', state.text)
		select = Select(self.browser.find_element_by_name('priority'))
		self.assertEqual([o.text for o in select.options], valid_priorities)
		selected_option = select.first_selected_option
		self.assertIn(selected_option.text, valid_priorities)
		# is there a better way to loop through datasources???
		# do we need to do all ????
		self.browser.get(URL + '/datasource/2')
		state = self.browser.find_element_by_name('state')
		self.assertIn(state.text, valid_states)
		self.assertIn('Awaiting Triage', state.text)

	def test_datagroup_list_length(self):
		b = len(DataGroup.objects.filter(data_source_id=1))
		self.browser.get(URL + '/datasource/1')
		row_count = len(self.browser.find_elements_by_xpath(
								"//table[@id='data_group_table']/tbody/tr"))
		# I'm getting vall from above, I can't seem to get the queryset to
		# return inside of this function
		self.assertEqual(b, row_count)


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
