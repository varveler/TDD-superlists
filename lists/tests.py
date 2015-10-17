from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page


# Create your tests here.

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		
		#resolve is the function Django uses interanlly to 
		#resolve URLS and find what view funciont should map to
		found = resolve('/')
		self.assertEqual(found.func, home_page)