from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
	
	@skip
	def test_cannot_add_empty_list_items(self):
		#Edith goes to home page and accidentaly tries to submit
		# an empty list item. She hits Enter on the empty input inbox

		#The home page refreshes and there is an error message saying
		# that list items cannot be blank

		#She tries againwith some text for the item, wich now works

		#Perversly, she now decides to submit a second blank list item.

		#She recieves a similar warning on the list page

		#And she can correct it by filling some text in
		self.fail('write me!')


#we removed this since now we are using python3 manage.py test functional_tests
#if __name__ == '__main__':
#	unittest.main(warnings='ignore')