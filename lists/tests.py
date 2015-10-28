from django.core.urlresolvers import resolve
from django.shortcuts import redirect, render
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item




# Create your tests here.

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		
		#resolve is the function Django uses interanlly to 
		#resolve URLS and find what view function should map to
		found = resolve('/')
		#here we are checking in the found url '/' django finds a function called home_page
		self.assertEqual(found.func, home_page)


	def test_home_page_return_correct_html(self):
		#HttpRequest is the object that the browser sees when the user
		#enter a page
		request = HttpRequest()

		#we pass that objetct to the home_page view and assing the variable response to it
		response = home_page(request)

		# the we want it to have these properties:
		# b stands for raw bites, not strings
		#self.assertTrue(response.content.startswith(b'<html>'))
		#self.assertIn(b'<title>To-Do lists</title>', response.content)
		#self.assertTrue(response.content.endswith(b'</html>'))

		# in order not to check constants we do the following code
		expected_html = render_to_string('home.html')
		# checks if the expected_html is the same as the request, decode() converts bytes into 
		#strings
		
		self.assertEqual(response.content.decode(), expected_html)
		print ("---> test home page return correct html")		

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)
		# Check if the objetc is in Items
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		# Check if the text is te same for first object
		self.assertEqual(new_item.text, "A new list item")

		# Check it the text is in the rendering of the page
		#self.assertIn('A new list item', response.content.decode())
		#expected_html = render_to_string(
        #								'home.html',
        #								{'new_item_text':  'A new list item'}
    	#							)
		# Check that the rendering of the page is correct, with the correct Item.text on it
		#self.assertEqual(response.content.decode(), expected_html)
		#print ('---> test home page can save a POST request')

		# 302 is the Redirect Code
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text']= 'A new list item'

		response = home_page(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


	def test_home_page_only_saves_items_when_necesary(self):
		request = HttpRequest()
		home_page(request)
		# No POST Request has made, check that there are no saved objects
		self.assertEqual(Item.objects.count(), 0)

	#def test_home_page_displays_all_list_items(self):
	#	Item.objects.create(text='itemey 1')
	#	Item.objects.create(text='itemey 2')

	#	request = HttpRequest()
	#	response = home_page(request)

	#	self.assertIn('itemey 1', response.content.decode())
	#	self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = "Item the second"
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, "Item the second")

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_all_items(self):
		# instead of using func test_home_page_displays_all_list_items
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		#instead of reuest = HttpRequest() and response = home_page(request)
		# we can pass the self.client wich is an atribute of the TestCase
		response = self.client.get('/lists/the-only-list-in-the-world/')

		#instead of using assertIn/response.content.decode() we use assertContains and
		# Django automatically knows to deal with the response
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')