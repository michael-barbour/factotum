import csv
import unittest
import collections
from selenium import webdriver
from selenium.webdriver.support.select import Select

from django.conf import settings
from django.utils import timezone
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile

from dashboard.models import DataGroup, DataSource, DataDocument

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
								"//table[@id='data_group_table']/tbody/tr"))
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

	def create_data_group(self, data_source, testusername = 'Karyn', name='Walmart MSDS 3', description='Another data group, added programatically'):
		source_csv = open('./sample_files/walmart_msds_3.csv','rb')
		return DataGroup.objects.create(name=name,
										description=description, data_source = data_source,
										downloaded_by=User.objects.get(username=testusername) ,
										downloaded_at=timezone.now(),
										csv=SimpleUploadedFile('walmart_msds_3.csv', source_csv.read() )
										)

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

	def create_data_documents(self, data_group):
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
						data_group=data_group)
					dds.append(dd)
			return dds

	# creation of another DataGroup from csv and pdf sources
	def test_new_data_group(self):
		# DataGroup, created using the model layer
		dg_count_before = DataGroup.objects.count()
		ds = DataSource.objects.get(pk=1)
		self.dg = self.create_data_group(data_source=ds)
		dg_count_after = DataGroup.objects.count()
		self.assertEqual(dg_count_after, dg_count_before + 1, "Confirm the DataGroup object has been created")
		self.assertEqual(3, self.dg.pk, "Confirm the new DataGroup object's pk is 3")
		self.pdfs = self.upload_pdfs()
		self.dds = self.create_data_documents(self.dg)

		# Use the browser layer to confirm that the object has been created
		self.browser.get('%s%s' % (self.live_server_url, '/datagroup/3'))
		self.assertEqual('factotum', self.browser.title,"Testing open of datagroup 3 show page")

		self.browser.get(self.live_server_url + reverse('data_group_detail', kwargs={'pk': self.dg.pk}))
		self.assertEqual('factotum', self.browser.title)
		h1 = self.browser.find_element_by_name('title')
		self.assertEqual('Walmart MSDS 3', h1.text)

		# Use the browser layer to delete the DataGroup object
		# deleting the DataGroup should clean up the file system
		self.browser.get(self.live_server_url + '/datagroup/delete/3')
		del_button = self.browser.find_elements_by_xpath('/html/body/div/form/input[2]')[0]
		del_button.click()
		self.assertEqual(DataGroup.objects.count(), dg_count_before , "Confirm the DataGroup object has been deleted")

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
		print(un_link.get_attribute("href"))
		self.assertEqual(un_link.get_attribute("href").split('/')[-1],str(ds.pk))
																	str(ds.pk))
