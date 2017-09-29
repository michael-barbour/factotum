from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from .views import index


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
		self.assertIn(b'<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">', response.content)
		self.assertIn(b'<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>', response.content)
		self.assertIn(b'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>', response.content)
		self.assertIn(b'<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>', response.content)

