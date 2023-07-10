from unittest import TestCase, main
from unittest.mock import patch

from pyrarcrack import generate_combinations
from pyrarcrack import advanced_generator


class TestCombination(TestCase):
    def test_should_generate_minimal_combination(self):
        self.assertEqual(
            list(generate_combinations('a', 1)),
            ['a']
        )

class TestAdvancedGenerator(TestCase):
    def test_should_generate_minimal_combination(self):
        self.assertEqual(
            list(advanced_generator([['a']])),
            ['a']
        )

    def test_should_not_fail_on_empty_alphabet(self):
        self.assertEqual(
            list(advanced_generator([])),
            []
        )

    def test_should_generate_2_char_combination(self):
        self.assertEqual(
            list(advanced_generator([['a','b'],['c','e']])),
            ['ac','ae','bc','be']
        )

    def test_should_generate_3_char_combination(self):
        self.assertEqual(
            list(advanced_generator([['a','b'],['c','e'],['d','f']])),
            ['acd','acf','aed','aef','bcd','bcf','bed','bef']
        )

if __name__ == '__main__':
    main()
