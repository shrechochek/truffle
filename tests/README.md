# TRUFFLE Tests

Comprehensive test suite to verify program correctness.

## Test Structure

### test_encoders.py (30+ tests)
Tests all encoding functions:
- Base64, Base58, Base32, Base45, Base62, Base85, Base92
- Hexadecimal
- Binary (with and without spaces)
- ROT (all 25 variants)
- Morse code
- Atbash cipher
- URL encoding

### test_decoders.py (35+ tests)
Tests all decoding functions:
- Correct decoding for each type
- Backward compatibility (encode → decode)
- Edge cases (empty strings, special characters)

### test_recursive.py (40+ tests)
Tests recursive decoding:
- Double encoding (depth 2)
- Triple encoding (depth 3)
- Combinations of different encoding types
- Reverse variants
- All ROT offsets with other encodings
- `_can_be_encoding()` function for optimization

### test_integration.py (15+ tests)
Integration tests through files:
- Search with depth 1
- Search with depth 2
- `-r` flag (disable ROT)
- Special cases (Morse, URL, Binary)
- Multiple matches

## Running Tests

### All tests at once
```bash
python tests/run_all_tests.py
```

### Individual modules
```bash
# Encoder tests
python -m unittest tests/test_encoders.py

# Decoder tests
python -m unittest tests/test_decoders.py

# Recursive decoding tests
python -m unittest tests/test_recursive.py

# Integration tests
python -m unittest tests/test_integration.py
```

### Specific test
```bash
python -m unittest tests.test_encoders.TestBase64Encoder.test_simple_text
```

### With verbose output
```bash
python -m unittest tests/test_encoders.py -v
```

## Test Coverage

| Module | Functions | Tests | Coverage |
|--------|-----------|-------|----------|
| encoders.py | 14 | 30+ | ~100% |
| decoders.py | 14 | 35+ | ~100% |
| core.py (recursive) | 4 | 40+ | ~95% |
| Integration | - | 15+ | ~90% |

**Total: ~120 tests**

## What is Tested

### Functionality
- ✅ All encoding/decoding types
- ✅ Recursive decoding (depth 2-3)
- ✅ Reverse variants
- ✅ ROT with different offsets
- ✅ Encoding combinations

### Edge Cases
- ✅ Empty strings
- ✅ Single characters
- ✅ Long texts (1000+ characters)
- ✅ Special characters
- ✅ Unicode characters

### Optimization
- ✅ `_can_be_encoding()` for all types
- ✅ Encoding type detection
- ✅ Skipping impossible combinations

### Integration
- ✅ Command line interface
- ✅ Reading from files
- ✅ `-i` and `-r` flags
- ✅ Result output

## Requirements

```bash
# Python 3.6+ standard library
# No additional dependencies required
```

## Example Output

### Successful run
```
test_base64_decode (tests.test_decoders.TestBase64Decoder) ... ok
test_double_base64 (tests.test_recursive.TestDoubleEncoding) ... ok
test_morse_code (tests.test_integration.TestIntegrationSpecialCases) ... ok

======================================================================
TEST STATISTICS
======================================================================
Total tests run: 120
Passed: 120
Failed: 0
Errors: 0
Skipped: 0
======================================================================
```

### On error
```
FAIL: test_base64_decode (tests.test_decoders.TestBase64Decoder)
----------------------------------------------------------------------
AssertionError: 'hello' != 'helo'

======================================================================
TEST STATISTICS
======================================================================
Total tests run: 120
Passed: 119
Failed: 1
Errors: 0
Skipped: 0
======================================================================
```

## Adding New Tests

### Test template
```python
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import encoders
import decoders

class TestNewFeature(unittest.TestCase):
    def test_something(self):
        # Arrange
        text = "test"
        
        # Act
        result = encoders.encode_base64(text)
        
        # Assert
        self.assertEqual(result, "dGVzdA==")

if __name__ == '__main__':
    unittest.main()
```

## CI/CD Integration

Tests can be easily integrated into CI/CD:

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: python tests/run_all_tests.py
```

## Debugging

To debug a specific test:
```python
# At the beginning of the test
import pdb; pdb.set_trace()
```

Or use verbose mode:
```bash
python -m unittest tests/test_encoders.py -v
```
