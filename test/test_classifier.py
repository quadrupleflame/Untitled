import unittest


class MyTestCase(unittest.TestCase):

    def test_init(self):
        pass

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
