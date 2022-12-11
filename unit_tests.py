import unittest
from src.query_expansion import preprocess, expand_query


class TestStringMethods(unittest.TestCase):

    def test_preprocess(self):
        self.assertEqual('foo', preprocess('FOO'))
        self.assertEqual('foo', preprocess('Foo!!!!'))

    def test_expand_query(self):
        self.assertEqual('dame', expand_query('lady'))
        self.assertEqual('mind intellectual reason', expand_query('intellect'))


if __name__ == '__main__':
    unittest.main()
