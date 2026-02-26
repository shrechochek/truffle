"""
Integration tests
Verifies the program works end-to-end through files
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import tempfile
import subprocess
import encoders


class TestIntegrationDepth1(unittest.TestCase):
    """Integration tests for depth 1"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_base64_search(self):
        """Search in Base64"""
        text = "flag{test123}"
        encoded = encoders.encode_base64(text)
        self.temp_file.write(f"Data: {encoded}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '1'],
            capture_output=True,
            text=True
        )
        
        self.assertIn('Found', result.stdout)
        self.assertIn('flag', result.stdout)
    
    def test_hex_search(self):
        """Search in Hex"""
        text = "secret"
        encoded = encoders.encode_hex(text)
        self.temp_file.write(f"Value: {encoded}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'secret', '-i', '1'],
            capture_output=True,
            text=True
        )
        
        self.assertIn('Found', result.stdout)


class TestIntegrationDepth2(unittest.TestCase):
    """Integration tests for depth 2"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_double_base64(self):
        """Double Base64"""
        text = "hello"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_base64(enc1)
        self.temp_file.write(f"Data: {enc2}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'hello', '-i', '2', '-r'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertIn('Found', result.stdout)
        self.assertIn('base64', result.stdout.lower())
    
    def test_base64_hex(self):
        """Base64 → Hex"""
        text = "test"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_hex(enc1)
        self.temp_file.write(f"Code: {enc2}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'test', '-i', '2', '-r'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertIn('Found', result.stdout)


class TestIntegrationNoRot(unittest.TestCase):
    """Tests for -r flag (disable ROT)"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_rot_disabled(self):
        """ROT disabled - should not find"""
        text = "flag"
        enc1 = encoders.encode_rot(text, 13)
        enc2 = encoders.encode_base64(enc1)
        self.temp_file.write(f"Data: {enc2}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '2', '-r'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # With -r flag should not find through ROT
        self.assertNotIn('rot', result.stdout.lower())
    
    def test_rot_enabled(self):
        """ROT enabled - should find"""
        text = "flag"
        enc1 = encoders.encode_rot(text, 13)
        enc2 = encoders.encode_base64(enc1)
        self.temp_file.write(f"Data: {enc2}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '2'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        self.assertIn('Found', result.stdout)


class TestIntegrationSpecialCases(unittest.TestCase):
    """Tests for special cases"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_morse_code(self):
        """Morse code"""
        text = "SOS"
        enc1 = encoders.encode_morse(text)
        enc2 = encoders.encode_base64(enc1)
        self.temp_file.write(f"Signal: {enc2}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'SOS', '-i', '2', '-r'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertIn('Found', result.stdout)
        self.assertIn('morse', result.stdout.lower())
    
    def test_url_encoding(self):
        """URL encoding"""
        text = "hello world"
        enc1 = encoders.encode_url(text)
        enc2 = encoders.encode_base64(enc1)
        self.temp_file.write(f"Link: {enc2}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'hello', '-i', '2', '-r'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertIn('Found', result.stdout)
    
    def test_binary_encoding(self):
        """Binary encoding"""
        text = "hi"
        enc1 = encoders.encode_binary(text, True)
        enc2 = encoders.encode_base64(enc1)
        self.temp_file.write(f"Binary: {enc2}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'hi', '-i', '2', '-r'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertIn('Found', result.stdout)


class TestIntegrationMultipleMatches(unittest.TestCase):
    """Tests for multiple matches"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_multiple_encodings(self):
        """Multiple different encodings in one file"""
        text = "flag"
        enc1 = encoders.encode_base64(text)
        enc2 = encoders.encode_hex(text)
        
        self.temp_file.write(f"First: {enc1}\n")
        self.temp_file.write(f"Second: {enc2}\n")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '1'],
            capture_output=True,
            text=True
        )
        
        # Should find both
        self.assertTrue(result.stdout.count('Found') >= 2)


if __name__ == '__main__':
    unittest.main()
