import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self, *args):
        print("ddd")
        pass

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
