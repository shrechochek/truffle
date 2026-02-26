"""
Tests for decoders.py module
Verifies correctness of all decoding functions
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import encoders
import decoders


class TestBase64Decoder(unittest.TestCase):
    def test_simple_decode(self):
        encoded = encoders.encode_base64("hello")
        decoded = decoders.decode_base64(encoded)
        self.assertEqual(decoded, "hello")
    
    def test_with_padding(self):
        decoded = decoders.decode_base64("aGVsbG8=")
        self.assertEqual(decoded, "hello")
    
    def test_without_padding(self):
        decoded = decoders.decode_base64("aGVsbG8")
        self.assertEqual(decoded, "hello")
    
    def test_empty(self):
        self.assertEqual(decoders.decode_base64(""), "")


class TestBase58Decoder(unittest.TestCase):
    def test_encode_decode(self):
        text = "test"
        encoded = encoders.encode_base58(text)
        decoded = decoders.decode_base58(encoded)
        self.assertEqual(decoded, text)
    
    def test_hello(self):
        text = "hello"
        encoded = encoders.encode_base58(text)
        decoded = decoders.decode_base58(encoded)
        self.assertEqual(decoded, text)


class TestBase32Decoder(unittest.TestCase):
    def test_encode_decode(self):
        text = "test"
        encoded = encoders.encode_base32(text)
        decoded = decoders.decode_base32(encoded)
        self.assertEqual(decoded, text)
    
    def test_with_padding(self):
        text = "a"
        encoded = encoders.encode_base32(text)
        decoded = decoders.decode_base32(encoded)
        self.assertEqual(decoded, text)


class TestHexDecoder(unittest.TestCase):
    def test_simple(self):
        decoded = decoders.decode_hex("6869")
        self.assertEqual(decoded, "hi")
    
    def test_encode_decode(self):
        text = "test123"
        encoded = encoders.encode_hex(text)
        decoded = decoders.decode_hex(encoded)
        self.assertEqual(decoded, text)


class TestRotDecoder(unittest.TestCase):
    def test_rot13(self):
        decoded = decoders.decode_rot("uryyb", 13)
        self.assertEqual(decoded, "hello")
    
    def test_rot1(self):
        decoded = decoders.decode_rot("bcd", 1)
        self.assertEqual(decoded, "abc")
    
    def test_encode_decode_rot13(self):
        text = "hello"
        encoded = encoders.encode_rot(text, 13)
        decoded = decoders.decode_rot(encoded, 13)
        self.assertEqual(decoded, text)
    
    def test_all_offsets(self):
        text = "test"
        for offset in range(1, 26):
            encoded = encoders.encode_rot(text, offset)
            decoded = decoders.decode_rot(encoded, offset)
            self.assertEqual(decoded, text)


class TestBinaryDecoder(unittest.TestCase):
    def test_with_spaces(self):
        encoded = encoders.encode_binary("hi", True)
        decoded = decoders.decode_binary(encoded)
        self.assertEqual(decoded, "hi")
    
    def test_without_spaces(self):
        encoded = encoders.encode_binary("hi", False)
        decoded = decoders.decode_binary(encoded)
        self.assertEqual(decoded, "hi")
    
    def test_single_char(self):
        encoded = encoders.encode_binary("a", True)
        decoded = decoders.decode_binary(encoded)
        self.assertEqual(decoded, "a")


class TestMorseDecoder(unittest.TestCase):
    def test_sos(self):
        encoded = encoders.encode_morse("SOS")
        decoded = decoders.decode_morse(encoded)
        self.assertEqual(decoded, "SOS")
    
    def test_hello(self):
        encoded = encoders.encode_morse("HELLO")
        decoded = decoders.decode_morse(encoded)
        self.assertEqual(decoded, "HELLO")
    
    def test_with_spaces(self):
        encoded = encoders.encode_morse("HI THERE")
        decoded = decoders.decode_morse(encoded)
        self.assertEqual(decoded, "HI THERE")


class TestAtbashDecoder(unittest.TestCase):
    def test_simple(self):
        decoded = decoders.decode_atbash("zyx")
        self.assertEqual(decoded, "abc")
    
    def test_encode_decode(self):
        text = "hello"
        encoded = encoders.encode_atbash(text)
        decoded = decoders.decode_atbash(encoded)
        self.assertEqual(decoded, text)


class TestUrlDecoder(unittest.TestCase):
    def test_space(self):
        decoded = decoders.decode_url("hello%20world")
        self.assertEqual(decoded, "hello world")
    
    def test_encode_decode(self):
        text = "test@example.com"
        encoded = encoders.encode_url(text)
        decoded = decoders.decode_url(encoded)
        self.assertEqual(decoded, text)
    
    def test_multiple_special(self):
        text = "a b c"
        encoded = encoders.encode_url(text)
        decoded = decoders.decode_url(encoded)
        self.assertEqual(decoded, text)


class TestNoDecoder(unittest.TestCase):
    def test_returns_same(self):
        text = "hello"
        self.assertEqual(decoders.no_decode(text), text)


if __name__ == '__main__':
    unittest.main()
