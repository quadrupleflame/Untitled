import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self, *args):
        pass

    def test_something(self):
        self.assertNotEqual(True, False)


if __name__ == '__main__':
    unittest.main()
