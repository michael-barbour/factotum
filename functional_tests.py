import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from factotum.settings_secret import USER, PW

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        '''You can't login!''' # docstrings get added to the failed test output
        # BELOW IS FROM THE USER PERSONAS
        # Dot needs to be able to track data sources so as not to duplicate
        # effort collecting a data source which is already included in the
        # database. She needs a way to easily deposit data in a common storage
        # location as she collects it. She also needs a way to see what the
        # team would like for her to prioritize in terms of her work.
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('login', self.browser.title)
        name = self.browser.find_element_by_id("id_username")
        name.send_keys(USER)
        name.send_keys(Keys.RETURN)
        pw = self.browser.find_element_by_id("id_password")
        pw.send_keys(PW)
        pw.send_keys(Keys.RETURN)
        self.assertIn('factotum', self.browser.title)

        # self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')



# browser = webdriver.Chrome()
# browser.get('http://127.0.0.1:8000/datagroup/8')
#
# assert 'login' in browser.title
#
# browser.close()
#
# browser = webdriver.Firefox()
# browser.get('http://localhost:8000')
#
# assert 'login' in browser.title
