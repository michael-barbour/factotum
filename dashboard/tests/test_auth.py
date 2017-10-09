from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from dashboard.views import index


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jdoe', email='jon.doe@epa.gov', password='Sup3r_secret')

    def test_login_goes_to_index(self):
        request = self.factory.get('/')
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_goes_to_login(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(response.content, b'Please sign in')
