from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import unittest
import time

#class NewVisitorTest(unittest.TestCase):
class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		# we tell the browsewr to implicitly wait 3 seconds
		self.browser.implicitly_wait(3)


	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):

		# Edith has heard about a cool new online to-do app. She goes
		# to check its homepage
		#self.browser.get('http://localhost:8000')
		self.browser.get(self.live_server_url)

		# She notices the page title and heade mentio to-do lists
		self.assertIn('To-Do lists', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
			)
		

		#She types "Buy peacock feathers" into a text box
		inputbox.send_keys('Buy peacock feathers')

		#When she hits Enter, the page updates and now the page lists
		# "1: Buy peacock feathers" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		
		#There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(4)
		# The page updates again, and now shows both items on her list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		self.fail('Finish the Tests!')

#Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some 
# explanatory text to that effect

# She visists that URL - her to-do list is still there

#Satsified she goes back to sleep


#we removed this since now we are using python3 manage.py test functional_tests
#if __name__ == '__main__':
#	unittest.main(warnings='ignore')