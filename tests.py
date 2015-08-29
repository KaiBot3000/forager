import unittest
import doctest
import server
from server import (function_test, )


# Also runs docTests in file
def load_tests(loader, tests, ignore):
    '''Loads and runs doctests from seperate file'''

    tests.addTests(doctest.DocTestSuite(server))
    tests.addTests(doctest.DocFileSuite('tests.txt'))

    return tests

class ForagerUnitTestCase(unittest.TestCase):

	def setUp(self):
		self.client = server.app.test_client()
		# test_client = server.app.test_client()

	def test_index(self):
		result = self.client.get('/')
		self.assertIn('<title>Forager</title>', result.data)

	def test_sign(self):
		result = self.client.get('/sign')
		self.assertIn('<title>Sign In/Up</title>', result.data)

	# def test_sign_in(self):
	# 	result = self.client.post('/sign', data={'username': 'fakeuser', 'password': '123'})
	# 	self.assertIn('<title>Sign In/Up</title>', result.data)

	# def test_sign_in(self):
	# 	result = self.client.post('/sign', date={'username': 'kai', 'password': '123'})
	# 	self.assertIn('<div id="search">', result.data)

	# def test_search_display(self):
	# 	result = self.client.get('/search?plant=all')
	# 	self.assertIn('<div id="search">', result.data)

	# def test_list_fields(self):
	# 	result = self.client.get('/list-fields')
	# 	self.assertIn('Apple', result.data)


if __name__ == '__main__':
    unittest.main()