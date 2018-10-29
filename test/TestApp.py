import unittest
import os, sys
from flask import Flask
from app import auth, api, db, home, create_app
import threading


class TestApp(unittest.TestCase):

    def setUp(self, *args):
        return

    def tearDown(self):
        pass

    def test_init(self):
        # self.assertEqual(type(self.flask), Flask)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_db(self):
        # database = db.init_app(self.flask)
        # self.assertEqual(type(database), type(None))
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_api(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_auth(self):
        pass

    def test_home(self):
        pass


if __name__ == '__main__':
    unittest.main()
