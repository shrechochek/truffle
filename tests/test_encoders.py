"""
Tests for encoders.py module
Verifies correctness of all encoding functions
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import encoders


class TestBase64Encoder(unittest.TestCase):
    def test_simple_text(self):
        self.assertEqual(encoders.encode_base64("hello"), "aGVsbG8=")
    
    def test_empty_string(self):
        self.assertEqual(encoders.encode_base64(""), "")
    
    def test_special_chars(self):
        result = encoders.encode_base64("hello world!")
        self.assertTrue(len(result) > 0)
    
    def test_unicode(self):
        result = encoders.encode_base64("привет")
        self.assertTrue(len(result) > 0)


class TestBase58Encoder(unittest.TestCase):
    def test_simple_text(self):
        result = encoders.encode_base58("test")
        self.assertNotIn('0', result)
        self.assertNotIn('O', result)
        self.assertNotIn('I', result)
        self.assertNotIn('l', result)
    
    def test_empty_string(self):
        result = encoders.encode_base58("")
        self.assertEqual(result, "")


class TestBase32Encoder(unittest.TestCase):
    def test_simple_text(self):
        result = encoders.encode_base32("hello")
        self.assertTrue(all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=' for c in result))
    
    def test_padding(self):
        result = encoders.encode_base32("a")
        self.assertTrue(result.endswith('='))


class TestHexEncoder(unittest.TestCase):
    def test_simple_text(self):
        self.assertEqual(encoders.encode_hex("hi"), "6869")
    
    def test_all_chars_hex(self):
        result = encoders.encode_hex("test")
        self.assertTrue(all(c in '0123456789abcdef' for c in result))


class TestRotEncoder(unittest.TestCase):
    def test_rot13(self):
        self.assertEqual(encoders.encode_rot("hello", 13), "uryyb")
    
    def test_rot13_reverse(self):
        self.assertEqual(encoders.encode_rot("uryyb", 13), "hello")
    
    def test_rot1(self):
        self.assertEqual(encoders.encode_rot("abc", 1), "bcd")
    
    def test_rot25(self):
        self.assertEqual(encoders.encode_rot("abc", 25), "zab")
    
    def test_uppercase(self):
        self.assertEqual(encoders.encode_rot("ABC", 13), "NOP")
    
    def test_mixed_case(self):
        self.assertEqual(encoders.encode_rot("HeLLo", 13), "UrYYb")
    
    def test_with_numbers(self):
        self.assertEqual(encoders.encode_rot("test123", 13), "grfg123")


class TestBinaryEncoder(unittest.TestCase):
    def test_simple_with_spaces(self):
        result = encoders.encode_binary("hi", True)
        self.assertIn(' ', result)
        self.assertTrue(all(c in '01 ' for c in result))
    
    def test_simple_without_spaces(self):
        result = encoders.encode_binary("hi", False)
        self.assertNotIn(' ', result)
        self.assertTrue(all(c in '01' for c in result))
    
    def test_length_with_spaces(self):
        result = encoders.encode_binary("a", True)
        self.assertEqual(len(result), 8)  # 8 bits
    
    def test_length_without_spaces(self):
        result = encoders.encode_binary("a", False)
        self.assertEqual(len(result), 8)


class TestMorseEncoder(unittest.TestCase):
    def test_sos(self):
        result = encoders.encode_morse("SOS")
        self.assertIn('...', result)
        self.assertIn('---', result)
    
    def test_hello(self):
        result = encoders.encode_morse("HELLO")
        self.assertTrue(all(c in '.- ' for c in result))
    
    def test_numbers(self):
        result = encoders.encode_morse("123")
        self.assertTrue(len(result) > 0)


class TestAtbashEncoder(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(encoders.encode_atbash("abc"), "zyx")
    
    def test_uppercase(self):
        self.assertEqual(encoders.encode_atbash("ABC"), "ZYX")
    
    def test_reverse(self):
        text = "hello"
        encoded = encoders.encode_atbash(text)
        decoded = encoders.encode_atbash(encoded)
        self.assertEqual(text, decoded)


class TestUrlEncoder(unittest.TestCase):
    def test_space(self):
        result = encoders.encode_url("hello world")
        self.assertIn('%20', result)
    
    def test_special_chars(self):
        result = encoders.encode_url("test@example.com")
        self.assertIn('%40', result)
    
    def test_safe_chars(self):
        result = encoders.encode_url("abc123")
        self.assertEqual(result, "abc123")


if __name__ == '__main__':
    unittest.main()
