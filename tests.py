import unittest
import doctest
from server import (fun_test, )

# Also runs docTests in file
# def load_tests(loader, tests, ignore):
#     """Also run our doctests and file-based doctests."""

#     tests.addTests(doctest.DocTestSuite(server))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests

class ForagerUnitTestCase(unittest.TestCase):

    def test_fun_test(self):
        self.assertEqual(fun_test(1, -1), 0)

    def test_search_display(self):
    	test_client = server.app.test_client()

    	result = test_client.get('/search')
    	self.assertIn("<div id='search'>", result.data)


if __name__ == "__main__":
    unittest.main()