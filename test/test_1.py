import unittest
import os
from app.model.classifier.Analyze import Analyze_content as Az
from flask import Flask
from app import auth, api, db, home, create_app


class TestAnalyze(unittest.TestCase):

    def test_init(self):
        app = create_app()
        self.assertEqual(type(app), Flask)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_db(self):
        app = create_app()
        database = db.init_app(app)
        self.assertEqual(type(database), type(None))
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
