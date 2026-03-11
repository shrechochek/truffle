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

    def test_plain_text_search(self):
        """Search in plain text"""
        self.temp_file.write("prefix flag suffix")
        self.temp_file.close()

        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '1'],
            capture_output=True,
            text=True
        )

        self.assertIn('Found', result.stdout)
        self.assertIn('no_decode', result.stdout)

    def test_vertical_plain_text_search(self):
        """Search in vertically aligned plain text"""
        self.temp_file.write("ф какой-то текст\n")
        self.temp_file.write("л какой\n")
        self.temp_file.write("а бла бла бла\n")
        self.temp_file.write("г тавыфаф\n")
        self.temp_file.close()

        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'флаг', '-i', '1'],
            capture_output=True,
            text=True
        )

        self.assertIn('Found', result.stdout)
        self.assertIn('флаг', result.stdout)

    def test_blind_search(self):
        """Blind search should find brace-wrapped text without explicit query"""
        self.temp_file.write("noise {some text} suffix")
        self.temp_file.close()

        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, '-i', '1', '-b'],
            capture_output=True,
            text=True
        )

        self.assertIn('Found', result.stdout)
        self.assertIn('{some text}', result.stdout)


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
            ['python', 'src/main.py', self.temp_file.name, 'hello', '-i', '2'],
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
            ['python', 'src/main.py', self.temp_file.name, 'test', '-i', '2'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertIn('Found', result.stdout)


class TestIntegrationRotFlag(unittest.TestCase):
    """Tests for -r flag (enable ROT)"""
    
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
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '2'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertNotIn('Found', result.stdout)
        self.assertNotIn('rot', result.stdout.lower())
    
    def test_rot_enabled(self):
        """ROT enabled - should find"""
        text = "flag"
        enc1 = encoders.encode_rot(text, 13)
        enc2 = encoders.encode_base64(enc1)
        self.temp_file.write(f"Data: {enc2}")
        self.temp_file.close()
        
        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '2', '-r'],
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
            ['python', 'src/main.py', self.temp_file.name, 'SOS', '-i', '2'],
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
            ['python', 'src/main.py', self.temp_file.name, 'hello', '-i', '2'],
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
            ['python', 'src/main.py', self.temp_file.name, 'hi', '-i', '2'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertIn('Found', result.stdout)

    def test_xor_encoding(self):
        """XOR encoding"""
        text = "flag"
        encoded = encoders.encode_xor(text, '-')
        self.temp_file.write(f"XOR: {encoded}")
        self.temp_file.close()

        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '1', '-x', '-'],
            capture_output=True,
            text=True,
            timeout=30
        )

        self.assertIn('Found', result.stdout)
        self.assertIn('xor', result.stdout.lower())

    def test_xor_base64_recursive(self):
        """XOR via recursive search"""
        text = "flag"
        enc1 = encoders.encode_xor(text, '-')
        enc2 = encoders.encode_base64(enc1)
        self.temp_file.write(f"Data: {enc2}")
        self.temp_file.close()

        result = subprocess.run(
            ['python', 'src/main.py', self.temp_file.name, 'flag', '-i', '2', '-x', '-'],
            capture_output=True,
            text=True,
            timeout=30
        )

        self.assertIn('Found', result.stdout)
        self.assertIn('xor', result.stdout.lower())


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


class TestIntegrationDeepSearch(unittest.TestCase):
    """Integration tests for deep recursive directory search"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_deep_search_finds_nested_file(self):
        """Deep mode should search recursively in nested directories"""
        nested_dir = os.path.join(self.temp_dir.name, 'level1', 'level2')
        os.makedirs(nested_dir)

        encoded = encoders.encode_base64('flag{nested}')
        target_file = os.path.join(nested_dir, 'payload.txt')
        with open(target_file, 'w') as f:
            f.write(f'Data: {encoded}')

        with open(os.path.join(self.temp_dir.name, 'ignore.txt'), 'w') as f:
            f.write('nothing to see here')

        result = subprocess.run(
            ['python', 'src/main.py', self.temp_dir.name, 'flag', '-i', '1', '-d'],
            capture_output=True,
            text=True,
            timeout=30
        )

        self.assertIn('Found', result.stdout)
        self.assertIn('payload.txt', result.stdout)


if __name__ == '__main__':
    unittest.main()
