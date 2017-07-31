import unittest
from util import *
from section import Section
from normalizer import Normalizer


class UtilTests(unittest.TestCase):
    def test_abbreviate_empty(self):
        self.assertIsNone(abbreviate([]))
        self.assertIsNone(abbreviate(None))

    def test_abbreviate(self):
        word_list_1 = ['hello', 'goodbye', '']
        word_list_2 = ['hello', '', 'goodbye']
        word_list_3 = ['hello', 'goodbye', '2']
        word_list_4 = ['hello', '2', 'goodbye', '']
        word_list_5 = ['', '']
        self.assertEqual(abbreviate(word_list_1), 'hg')
        self.assertEqual(abbreviate(word_list_2), 'hg')
        self.assertEqual(abbreviate(word_list_3), 'hg2')
        self.assertEqual(abbreviate(word_list_4), 'h2g')
        self.assertEqual(abbreviate(word_list_5), "")

    def test_tokenize_empty(self):
        self.assertIsNone(tokenize(None))
        self.assertIsNone(tokenize(''))

    def test_tokenize(self):
        word_1 = "hello 5"
        word_2 = "5"
        word_3 = "test 5 another"
        word_4 = "test another"
        self.assertEqual(tokenize(word_1), ["hello"])
        self.assertIsNone(tokenize(word_2))
        self.assertEqual(tokenize(word_3), ['test', 'another'])
        self.assertEqual(tokenize(word_4), ['test', 'another'])

    def test_extract_number_empty(self):
        self.assertIsNone(extract_number(""))
        self.assertIsNone(extract_number(None))

    def test_extract_number(self):
        self.assertEqual(extract_number("test 5"), "5")
        self.assertEqual(extract_number("test 001"), "001")
        self.assertEqual(extract_number("001 test"), "001")
        self.assertEqual(extract_number("test 00"), "00")
        self.assertIsNone(extract_number("1 test 2"))
        self.assertIsNone(extract_number("1 2"))

    def test_fuzzy_chooser(self):
        tokens = ["pineapple", "shoe"]
        sections_1 = [Section("pineapple 10", 1, extract_number), Section("west 5", 2, extract_number)]
        sections_2 = [Section("banana 10", 1, extract_number), Section("west 5", 2, extract_number)]
        self.assertEqual(fuzzy_section_chooser(tokens, sections_1), sections_1[0])
        self.assertIsNone(fuzzy_section_chooser(tokens, sections_2))
        sections_1.append(Section("pineapple shoe 15", 3, extract_number))
        self.assertEqual(fuzzy_section_chooser(tokens, sections_1), sections_1[2])


class NormalizationTests(unittest.TestCase):
    def setUp(self):
        self.test_normalizer = Normalizer()
        self.test_normalizer.read_manifest("./test_manifest.csv")

    def test_load_manifest(self):
        self.assertEqual(len(self.test_normalizer.sections_full), 6)
        self.assertEqual(len(self.test_normalizer.sections_abbrev), 6)
        section_one = self.test_normalizer.sections_full["one 1"]
        self.assertEqual(len(section_one.rows), 3)

    def test_simple_normalization(self):
        self.assertEqual(self.test_normalizer.normalize("one 1", "1"), (1, 0, True))

    def no_match(self):
        self.assertEqual(self.test_normalizer.normalize("one 1", "1"), (1, 0, True))

    def match_section_only(self):
        self.assertEqual(self.test_normalizer.normalize("one 1", "10"), (1, None, False))

    def match_number_only(self):
        self.assertEqual(self.test_normalizer.normalize("1", "1"), (1, 0, True))

    def match_initials(self):
        self.assertEqual(self.test_normalizer.normalize("rf5", "1"), (5, 0, True))

    def match_missing_token(self):
        self.assertEqual(self.test_normalizer.normalize("right 5", "1"), (5, 0, True))

    def match_missing_token_2(self):
        self.assertEqual(self.test_normalizer.normalize("right 4", "1"), (6, 0, True))

    def no_match_row_dash(self):
        self.assertEqual(self.test_normalizer.normalize("rf5", "1-2"), (5, None, False))

    def no_match_at_all(self):
        self.assertEqual(self.test_normalizer.normalize("shoelace 5", "1"), (None, None, False))