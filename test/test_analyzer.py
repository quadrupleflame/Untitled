from unittest import TestCase
from app.model.hate_speech.process import Analyzer
import os


class TestAnalyzer(TestCase):

    def setUp(self):
        self.analyzer = Analyzer()
        os.chdir("..\\model\\hate_speech\\")

    def test_preprocess(self):

        url1 = "http://www.google.com/"
        self.assertEqual(Analyzer.preprocess(url1), "URLHERE")

        mention1 = "@wow"
        self.assertEqual(Analyzer.preprocess(mention1), "MENTIONHERE")

        space1 = "                 "
        space2 = ""
        space3 = " "
        self.assertEqual(Analyzer.preprocess(space1), " ")
        self.assertNotEqual(Analyzer.preprocess(space2), " ")
        self.assertEqual(Analyzer.preprocess(space1), Analyzer.preprocess(space3))
        self.fail()

    def test_tokenize(self):
        pass

    def test_basic_tokenize(self):
        pass

    def test_get_pos_tags(self):
        pass

    def test_other_features_(self):
        pass

    def test_count_twitter_objs(self):
        pass

    def test_get_oth_features(self):
        pass

    def test_transform_inputs(self):
        pass

    def test_predictions(self):
        pass

    def test_get_text_predictions(self):
        pass

    def test__text_predictions(self):
        pass

    def test_get_url_predictions(self):
        pass
