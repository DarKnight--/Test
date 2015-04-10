from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		#visit the homepage
		self.browser.get(self.live_server_url)
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
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')	
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		# Use peacock feather to make a fly is added in list
		inputbox.send_keys('Use peacock feathers to make a fly')
                # When enter is hit the page adds a to-do item
		inputbox.send_keys(Keys.ENTER)
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.browser.quit()

		# Now a new user visits the home page, there is no sign of other's list
		self.browser = webdriver.Firefox()
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
		#new user creates his own list
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		#new user gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, 'lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)
		self.fail('finish the test!')
