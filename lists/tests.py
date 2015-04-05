from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

# Create your tests here.

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_vies(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')		
		self.assertEqual(response.content.decode(), expected_html)
	
	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		response = home_page(request)
		self.assertIn('A new list item', response.content.decode())


class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()
	
		saved_item = Item.objects.all()
		self.assertEqual(saved_item.count(), 2)
		
		self.assertEqual(saved_item[0].text, 'The first (ever) list item')
		self.assertEqual(saved_item[1].text, 'Item the second')
