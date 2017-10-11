from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from dashboard.views import index
from django.contrib.auth.models import User


class IndexTestPage(TestCase):

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.user = User.objects.create_user(
			username='jdoe', email='jon.doe@epa.gov', password='Sup3r_secret')
		self.client.login(username='jdoe', password='Sup3r_secret')

	def test_root_url_resolves_to_dashboard(self):
		found = resolve('/')
		self.assertEqual(found.func, index)

	def test_dashboard_html_includes(self):
		response = self.client.get('/', follow=True)
		# Setting up valid HTML
		self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
		self.assertIn(b'<title>factotum</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))

	def test_dashboard_has_bootstrap(self):
		response = self.client.get('/', follow=True)
		# using CDN ensure that css and js for bootstrap is loaded.
		self.assertIn(b'<link rel="stylesheet" href="/static/css/bootstrap.min.css"', response.content)
		self.assertIn(b'<script src="/static/js/jquery-3.2.1.min.js"', response.content)
		self.assertIn(b'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js',
					  response.content)
		self.assertIn(b'<script src="/static/js/bootstrap.min.js', response.content)
