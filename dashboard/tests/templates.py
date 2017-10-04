from django.test import TestCase, SimpleTestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from dashboard.views import index


class IndexTestPage(TestCase):

	def test_root_url_resolves_to_dashboard(self):
		found = resolve('/')
		self.assertEqual(found.func, index)

	def test_dashboard_html_includes(self):
		request = HttpRequest()
		response = index(request)
		# Setting up valid HTML
		self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
		self.assertIn(b'<title>factotum</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))

	def test_dashboard_has_bootstrap(self):
		request = HttpRequest()
		response = index(request)
		# using CDN ensure that css and js for bootstrap is loaded.
		self.assertIn(b'<link rel="stylesheet" href="/static/css/bootstrap.min.css"', response.content)
		self.assertIn(b'<script src="/static/js/jquery-3.2.1.min.js"', response.content)
		self.assertIn(b'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>', response.content)
		self.assertIn(b'<script src="/static/js/bootstrap.min.js', response.content)

class AuthorizationTest(TestCase):

	def test_dashboard_not_signed_in_resolves_to_login(self):
		# if you go to the root page (index) and are not signed in you are redirected
		# to login page
		request = HttpRequest()
		response = index(request)

