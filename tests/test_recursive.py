"""
Tests for recursive decoding
Verifies functionality with multiple encoding layers
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import tempfile
import encoders
import decoders
import core


class TestDoubleEncoding(unittest.TestCase):
    """Tests for double encoding (depth 2)"""
    
    def test_base64_base64(self):
        """Base64 → Base64"""
        text = "secret"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_base64(enc1)
        
        # Проверяем декодирование
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_base64(dec1)
        self.assertEqual(dec2, text)
    
    def test_base64_base58(self):
        """Base64 → Base58"""
        text = "test"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_base58(enc1)
        
        dec1 = decoders.decode_base58(enc2)
        dec2 = decoders.decode_base64(dec1)
        self.assertEqual(dec2, text)
    
    def test_hex_base64(self):
        """Hex → Base64"""
        text = "hello"
        enc1 = encoders.encode_hex(text)
        enc2 = encoders.encode_base64(enc1)
        
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_hex(dec1)
        self.assertEqual(dec2, text)
    
    def test_rot13_base64(self):
        """ROT13 → Base64"""
        text = "flag"
        enc1 = encoders.encode_rot(text, 13)
        enc2 = encoders.encode_base64(enc1)
        
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_rot(dec1, 13)
        self.assertEqual(dec2, text)
    
    def test_base64_hex(self):
        """Base64 → Hex"""
        text = "data"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_hex(enc1)
        
        dec1 = decoders.decode_hex(enc2)
        dec2 = decoders.decode_base64(dec1)
        self.assertEqual(dec2, text)


class TestTripleEncoding(unittest.TestCase):
    """Tests for triple encoding (depth 3)"""
    
    def test_base64_base64_base64(self):
        """Base64 → Base64 → Base64"""
        text = "test"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_base64(enc1)
        enc3 = encoders.encode_base64(enc2)
        
        dec1 = decoders.decode_base64(enc3)
        dec2 = decoders.decode_base64(dec1)
        dec3 = decoders.decode_base64(dec2)
        self.assertEqual(dec3, text)
    
    def test_hex_base64_base58(self):
        """Hex → Base64 → Base58"""
        text = "abc"
        enc1 = encoders.encode_hex(text)
        enc2 = encoders.encode_base64(enc1)
        enc3 = encoders.encode_base58(enc2)
        
        dec1 = decoders.decode_base58(enc3)
        dec2 = decoders.decode_base64(dec1)
        dec3 = decoders.decode_hex(dec2)
        self.assertEqual(dec3, text)


class TestReverseEncoding(unittest.TestCase):
    """Tests for encoding with reverse"""
    
    def test_base64_reverse(self):
        """Base64 → Reverse"""
        text = "hello"
        enc1 = encoders.encode_base64(text)
        enc2 = enc1[::-1]
        
        dec1 = enc2[::-1]
        dec2 = decoders.decode_base64(dec1)
        self.assertEqual(dec2, text)
    
    def test_base64_reverse_base64(self):
        """Base64 → Reverse → Base64"""
        text = "test"
        enc1 = encoders.encode_base64(text)
        enc2 = enc1[::-1]
        enc3 = encoders.encode_base64(enc2)
        
        dec1 = decoders.decode_base64(enc3)
        dec2 = dec1[::-1]
        dec3 = decoders.decode_base64(dec2)
        self.assertEqual(dec3, text)


class TestSpecialEncodings(unittest.TestCase):
    """Tests for special encoding types"""
    
    def test_morse_base64(self):
        """Morse → Base64"""
        text = "SOS"
        enc1 = encoders.encode_morse(text)
        enc2 = encoders.encode_base64(enc1)
        
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_morse(dec1)
        self.assertEqual(dec2, text)
    
    def test_url_base64(self):
        """URL → Base64"""
        text = "hello world"
        enc1 = encoders.encode_url(text)
        enc2 = encoders.encode_base64(enc1)
        
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_url(dec1)
        self.assertEqual(dec2, text)
    
    def test_binary_base64(self):
        """Binary → Base64"""
        text = "hi"
        enc1 = encoders.encode_binary(text, True)
        enc2 = encoders.encode_base64(enc1)
        
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_binary(dec1)
        self.assertEqual(dec2, text)
    
    def test_atbash_base64(self):
        """Atbash → Base64"""
        text = "test"
        enc1 = encoders.encode_atbash(text)
        enc2 = encoders.encode_base64(enc1)
        
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_atbash(dec1)
        self.assertEqual(dec2, text)


class TestAllRotOffsets(unittest.TestCase):
    """Tests for all ROT variants"""
    
    def test_all_rot_with_base64(self):
        """Check all ROT offsets with Base64"""
        text = "hello"
        for offset in range(1, 26):
            with self.subTest(offset=offset):
                enc1 = encoders.encode_rot(text, offset)
                enc2 = encoders.encode_base64(enc1)
                
                dec1 = decoders.decode_base64(enc2)
                dec2 = decoders.decode_rot(dec1, offset)
                self.assertEqual(dec2, text)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases"""
    
    def test_single_char(self):
        """Single character"""
        text = "a"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_base64(enc1)
        
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_base64(dec1)
        self.assertEqual(dec2, text)
    
    def test_long_text(self):
        """Long text"""
        text = "a" * 1000
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_base64(enc1)
        
        dec1 = decoders.decode_base64(enc2)
        dec2 = decoders.decode_base64(dec1)
        self.assertEqual(dec2, text)
    
    def test_special_characters(self):
        """Special characters"""
        text = "!@#$%^&*()"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_hex(enc1)
        
        dec1 = decoders.decode_hex(enc2)
        dec2 = decoders.decode_base64(dec1)
        self.assertEqual(dec2, text)


class TestCanBeEncoding(unittest.TestCase):
    """Tests for _can_be_encoding function"""
    
    def test_url_detection(self):
        """Check URL encoding detection"""
        self.assertTrue(core._can_be_encoding("test%20data", "url"))
        self.assertFalse(core._can_be_encoding("testdata", "url"))
    
    def test_morse_detection(self):
        """Check Morse detection"""
        self.assertTrue(core._can_be_encoding("... --- ...", "morse"))
        self.assertFalse(core._can_be_encoding("abc123", "morse"))
    
    def test_binary_detection(self):
        """Check Binary detection"""
        self.assertTrue(core._can_be_encoding("01010101", "binary"))
        self.assertFalse(core._can_be_encoding("abc", "binary"))
    
    def test_hex_detection(self):
        """Check Hex detection"""
        self.assertTrue(core._can_be_encoding("48656c6c6f", "hex"))
        self.assertFalse(core._can_be_encoding("hello", "hex"))
    
    def test_base64_detection(self):
        """Check Base64 detection"""
        self.assertTrue(core._can_be_encoding("aGVsbG8=", "base64"))
        self.assertFalse(core._can_be_encoding("hello!", "base64"))
    
    def test_base58_detection(self):
        """Check Base58 detection"""
        self.assertTrue(core._can_be_encoding("3vQB7T", "base58"))
        self.assertFalse(core._can_be_encoding("0OIl", "base58"))


if __name__ == '__main__':
    unittest.main()
