"""
Tests for edge cases and special situations
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import encoders
import decoders


class TestEmptyStrings(unittest.TestCase):
    """Tests for empty strings"""
    
    def test_base64_empty(self):
        self.assertEqual(encoders.encode_base64(""), "")
        self.assertEqual(decoders.decode_base64(""), "")
    
    def test_base58_empty(self):
        self.assertEqual(encoders.encode_base58(""), "")
        self.assertEqual(decoders.decode_base58(""), "")
    
    def test_hex_empty(self):
        self.assertEqual(encoders.encode_hex(""), "")
        self.assertEqual(decoders.decode_hex(""), "")


class TestSingleCharacter(unittest.TestCase):
    """Tests for single characters"""
    
    def test_base64_single(self):
        for char in "abcABC123":
            with self.subTest(char=char):
                encoded = encoders.encode_base64(char)
                decoded = decoders.decode_base64(encoded)
                self.assertEqual(decoded, char)
    
    def test_hex_single(self):
        for char in "abcABC123":
            with self.subTest(char=char):
                encoded = encoders.encode_hex(char)
                decoded = decoders.decode_hex(encoded)
                self.assertEqual(decoded, char)
    
    def test_rot_single(self):
        for char in "abcxyz":
            with self.subTest(char=char):
                encoded = encoders.encode_rot(char, 13)
                decoded = decoders.decode_rot(encoded, 13)
                self.assertEqual(decoded, char)


class TestLongStrings(unittest.TestCase):
    """Tests for long strings"""
    
    def test_base64_long(self):
        text = "a" * 10000
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)
    
    def test_hex_long(self):
        text = "test" * 1000
        encoded = encoders.encode_hex(text)
        decoded = decoders.decode_hex(encoded)
        self.assertEqual(decoded, text)
    
    def test_rot_long(self):
        text = "hello" * 500
        encoded = encoders.encode_rot(text, 13)
        decoded = decoders.decode_rot(encoded, 13)
        self.assertEqual(decoded, text)


class TestSpecialCharacters(unittest.TestCase):
    """Tests for special characters"""
    
    def test_punctuation(self):
        text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)
    
    def test_newlines(self):
        text = "line1\nline2\nline3"
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)
    
    def test_tabs(self):
        text = "col1\tcol2\tcol3"
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)


class TestMixedCase(unittest.TestCase):
    """Tests for mixed case"""
    
    def test_rot_mixed(self):
        text = "HeLLo WoRLd"
        encoded = encoders.encode_rot(text, 13)
        decoded = decoders.decode_rot(encoded, 13)
        self.assertEqual(decoded, text)
    
    def test_atbash_mixed(self):
        text = "TeSt"
        encoded = encoders.encode_atbash(text)
        decoded = decoders.decode_atbash(encoded)
        self.assertEqual(decoded, text)


class TestNumbers(unittest.TestCase):
    """Tests for numbers"""
    
    def test_only_numbers(self):
        text = "1234567890"
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)
    
    def test_hex_numbers(self):
        text = "42"
        encoded = encoders.encode_hex(text)
        decoded = decoders.decode_hex(encoded)
        self.assertEqual(decoded, text)
    
    def test_rot_preserves_numbers(self):
        text = "test123"
        encoded = encoders.encode_rot(text, 13)
        self.assertIn("123", encoded)


class TestWhitespace(unittest.TestCase):
    """Tests for whitespace characters"""
    
    def test_spaces(self):
        text = "hello world"
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)
    
    def test_multiple_spaces(self):
        text = "a    b    c"
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)
    
    def test_leading_trailing_spaces(self):
        text = "  test  "
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)


class TestRepeatingPatterns(unittest.TestCase):
    """Tests for repeating patterns"""
    
    def test_repeated_char(self):
        text = "aaaaaaaaaa"
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)
    
    def test_repeated_pattern(self):
        text = "abcabc" * 10
        encoded = encoders.encode_base64(text)
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, text)


class TestBinaryEdgeCases(unittest.TestCase):
    """Tests for Binary encoding"""
    
    def test_binary_all_zeros(self):
        # Character with code 0 (null)
        text = "\x00"
        encoded = encoders.encode_binary(text, False)
        self.assertEqual(encoded, "00000000")
    
    def test_binary_all_ones(self):
        # Character with code 255
        text = "\xff"
        encoded = encoders.encode_binary(text, False)
        self.assertEqual(encoded, "11111111")


class TestMorseEdgeCases(unittest.TestCase):
    """Tests for Morse encoding"""
    
    def test_morse_numbers(self):
        text = "123"
        encoded = encoders.encode_morse(text)
        decoded = decoders.decode_morse(encoded)
        self.assertEqual(decoded, text)
    
    def test_morse_punctuation(self):
        text = "."
        encoded = encoders.encode_morse(text)
        decoded = decoders.decode_morse(encoded)
        self.assertEqual(decoded, text)


class TestUrlEdgeCases(unittest.TestCase):
    """Tests for URL encoding"""
    
    def test_url_multiple_spaces(self):
        text = "a b c"
        encoded = encoders.encode_url(text)
        self.assertEqual(encoded.count("%20"), 2)
    
    def test_url_special_chars(self):
        text = "test@example.com"
        encoded = encoders.encode_url(text)
        decoded = decoders.decode_url(encoded)
        self.assertEqual(decoded, text)
    
    def test_url_already_encoded(self):
        text = "test%20data"
        encoded = encoders.encode_url(text)
        # % should be encoded as %25
        self.assertIn("%25", encoded)


if __name__ == '__main__':
    unittest.main()
