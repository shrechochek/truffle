import encoders

# === decoders ===

def decode_base58(data: str) -> str:
    ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    padding = len(data) - len(data.lstrip(ALPHABET[0]))
    num = 0
    for char in data:
        if char not in ALPHABET:
            continue
        num = num * 58 + ALPHABET.index(char)
    
    try:
        res_bytes = num.to_bytes((num.bit_length() + 7) // 8, 'big')
        return (b'\0' * padding + res_bytes).decode('utf-8')
    except (UnicodeDecodeError, OverflowError):
        return ""

def decode_base64(data: str) -> str:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    data = data.rstrip('=')
    
    buffer = 0
    bits_count = 0
    res_bytes = bytearray()
    
    for char in data:
        if char not in ALPHABET:
            continue
        buffer = (buffer << 6) | ALPHABET.index(char)
        bits_count += 6
        if bits_count >= 8:
            bits_count -= 8
            res_bytes.append((buffer >> bits_count) & 0xFF)
    
    try:
        return res_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return ""

def decode_base32(data: str) -> str:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    data = data.rstrip('=')
    
    binary_str = ""
    for char in data:
        if char not in ALPHABET:
            continue
        val = ALPHABET.index(char)
        binary_str += f"{val:05b}"
    
    res_bytes = bytearray()
    for i in range(0, (len(binary_str) // 8) * 8, 8):
        res_bytes.append(int(binary_str[i:i+8], 2))
    
    try:
        return res_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return ""

def decode_base45(data: str) -> str:
    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
    res_bytes = bytearray()
    
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        try:
            if len(chunk) == 3:
                if all(c in ALPHABET for c in chunk):
                    val = ALPHABET.index(chunk[0]) + \
                          ALPHABET.index(chunk[1]) * 45 + \
                          ALPHABET.index(chunk[2]) * 45 * 45
                    res_bytes.append(val >> 8)
                    res_bytes.append(val & 0xFF)
            else: # последний блок из 2 символов
                if all(c in ALPHABET for c in chunk):
                    val = ALPHABET.index(chunk[0]) + ALPHABET.index(chunk[1]) * 45
                    res_bytes.append(val)
        except ValueError:
            continue
    
    try:
        return res_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return ""

def decode_base62(data: str) -> str:
    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    num = 0
    for char in data:
        if char not in ALPHABET:
            continue
        num = num * 62 + ALPHABET.index(char)
    
    try:
        return num.to_bytes((num.bit_length() + 7) // 8, 'big').decode('utf-8')
    except (UnicodeDecodeError, OverflowError):
        return ""

def decode_base85(data: str) -> str:
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
    res_bytes = bytearray()
    
    for i in range(0, len(data), 5):
        chunk = data[i:i+5]
        if not all(c in ALPHABET for c in chunk):
            continue
        val = 0
        for char in chunk:
            val = val * 85 + ALPHABET.index(char)
        try:
            res_bytes.extend(val.to_bytes(4, 'big'))
        except OverflowError:
            continue
    
    try:
        return res_bytes.rstrip(b'\0').decode('utf-8')
    except UnicodeDecodeError:
        return ""

def decode_base92(data: str) -> str:
    ALPHABET = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
               "[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    num = 0
    for char in data:
        if char not in ALPHABET:
            continue
        num = num * 92 + ALPHABET.index(char)
    
    try:
        return num.to_bytes((num.bit_length() + 7) // 8, 'big').decode('utf-8')
    except (UnicodeDecodeError, OverflowError):
        return ""

def decode_hex(data: str) -> str:
    res_bytes = bytearray()
    for i in range(0, len(data), 2):
        try:
            res_bytes.append(int(data[i:i+2], 16))
        except ValueError:
            continue
    try:
        return res_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return ""

def decode_rot(data: str, offset: int) -> str:
    return encoders.encode_rot(data, -offset)

def decode_binary(data: str) -> str:
    data = data.replace(" ", "")
    res_bytes = bytearray()
    for i in range(0, len(data), 8):
        try:
            res_bytes.append(int(data[i:i+8], 2))
        except ValueError:
            continue
    try:
        return res_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return ""

def decode_morse(data: str) -> str:
    MORSE_CODE_DICT = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
        '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
        '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
        '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
        '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
        '----.': '9', '-----': '0', '.-.-.-': '.', '--..--': ',', '..--..': '?',
        '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')'
    }
    
    words = data.split('  ')
    decoded_message = []
    
    for word in words:
        chars = word.split(' ')
        decoded_word = "".join(MORSE_CODE_DICT.get(c, c) for c in chars)
        decoded_message.append(decoded_word)
        
    return " ".join(decoded_message)

def decode_atbash(data: str) -> str:
    return encoders.encode_atbash(data)

def decode_url(data: str) -> str:
    result = bytearray()
    i = 0
    while i < len(data):
        try:
            if data[i] == '%' and i + 2 < len(data):
                result.append(int(data[i+1:i+3], 16))
                i += 3
            else:
                result.append(ord(data[i]))
                i += 1
        except (ValueError, OverflowError):
            i += 1
            continue
    try:
        return result.decode('utf-8')
    except UnicodeDecodeError:
        return ""

def do_nothing(data: str) -> str:
    return data