import unittest
from src.query_expansion import preprocess, expand_query


class TestStringMethods(unittest.TestCase):

    def test_preprocess(self):  # tests to check normalization via the preprocess function
        self.assertEqual('foo', preprocess('FOO'))
        self.assertEqual('foo', preprocess('Foo!!!!'))

    def test_expand_query(self):  # tests to check query expansion
        self.assertEqual('dame', expand_query('lady'))
        self.assertEqual('cerebral', expand_query('intellectual'))


if __name__ == '__main__':
    unittest.main()
