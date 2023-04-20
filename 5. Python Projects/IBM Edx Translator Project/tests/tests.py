import unittest
from translator import english_to_french, english_to_german

class translator(unittest.TestCase):

    def test_null_input(self):
        self.assertEqual(english_to_french(''), '')

    def test_hello_translation(self):
        self.assertEqual(english_to_french('Hello'), 'Bonjour')

    def test_long_text_translation(self):
        english_text = 'Hello everyone'
        french_text = 'Bonjour tout le monde'
        self.assertEqual(english_to_french(english_text), french_text)

    def test_null_input(self):
        self.assertEqual(english_to_german(''), '')

    def test_hello_translation(self):
        self.assertEqual(english_to_german('Hello'), 'Hallo')

    def test_long_text_translation(self):
        english_text = 'Hello everyone'
        german_text = 'Hallo alle'
        self.assertEqual(english_to_german(english_text), german_text)

if __name__ == '__main__':
    unittest.main()
