from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page




# Create your tests here.

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		
		#resolve is the function Django uses interanlly to 
		#resolve URLS and find what view funciont should map to
		found = resolve('/')
		self.assertEqual(found.func, home_page)


	def test_home_page_return_correct_html(self):
		#HTTPRequest is the object that the browser sees when the user
		#enter a page
		request = HttpRequest()

		#we pass that objetct to the home_page view and assing the variable response to it
		response = home_page(request)

		# the we want it to have these properties:
		# b stands for raw bites, not strings
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<tittle>To-Do lists</tittle>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))