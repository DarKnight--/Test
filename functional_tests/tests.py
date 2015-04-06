from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		#visit the homepage
		self.browser.get('http://localhost:8000')
		# Notice the title and header
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		# invited to enter a to-do item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		
		# Buy peacock feathers is added in list
		inputbox.send_keys('Buy peacock feathers')
		# When enter is hit the page adds a to-do item
		inputbox.send_keys(Keys.ENTER)	
		# Use peacock feather to make a fly is added in list
		inputbox.send_keys('Use peacock feathers to make a fly')
                # When enter is hit the page adds a to-do item
		inputbox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(
			any(row.text == '1: Buy peacock feathers' for row in rows)
		)
		self.assertIn(
                        any(row.text == '2: Use peacock feathers to make a fly' for row in rows)
                )
		
		self.fail('finish the test!')


if __name__ == '__main__':
	unittest.main(warnings='ignore')
