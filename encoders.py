# === encoders ===

def encode_base58(data: str) -> str:
    ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    if isinstance(data, str): data = data.encode('utf-8')
    padding = len(data) - len(data.lstrip(b'\0'))
    
    num = int.from_bytes(data, 'big')
    
    result = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        result = ALPHABET[remainder] + result
    
    return (ALPHABET[0] * padding) + result

def encode_base64(data: str) -> str:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    if isinstance(data, str): data = data.encode('utf-8')
    
    result = ""
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
        
        buffer = int.from_bytes(chunk, 'big') << (8 * (3 - len(chunk)))
        
        for j in range(4):
            if i * 8 + j * 6 < len(data) * 8:
                index = (buffer >> (18 - j * 6)) & 0x3F
                result += ALPHABET[index]
            else:
                result += "="
                
    return result

def encode_base32(data: str) -> str:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    if isinstance(data, str): data = data.encode('utf-8')

    binary_str = "".join(f"{b:08b}" for b in data)
    
    padding_bits = (5 - len(binary_str) % 5) % 5
    binary_str += "0" * padding_bits
    
    result = ""
    for i in range(0, len(binary_str), 5):
        chunk = binary_str[i:i+5]
        result += ALPHABET[int(chunk, 2)]
    
    while len(result) % 8 != 0:
        result += "="
        
    return result

def encode_base45(data: str) -> str:
    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
    if isinstance(data, str): data = data.encode('utf-8')
    
    result = ""
    for i in range(0, len(data) - 1, 2):
        val = (data[i] << 8) + data[i+1]
        
        c, rem = divmod(val, 45 * 45)
        b, a = divmod(rem, 45)
        result += ALPHABET[a] + ALPHABET[b] + ALPHABET[c]
        
    if len(data) % 2 != 0:
        val = data[-1]
        b, a = divmod(val, 45)
        result += ALPHABET[a] + ALPHABET[b]
        
    return result

def encode_base62(data: str) -> str:
    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if isinstance(data, str): data = data.encode('utf-8')
    
    num = int.from_bytes(data, 'big')
    if num == 0: return ALPHABET[0]
    
    result = ""
    while num > 0:
        num, rem = divmod(num, 62)
        result = ALPHABET[rem] + result

    return result

def encode_base85(data: str) -> str:
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
    if isinstance(data, str): data = data.encode('utf-8')
    
    padding = (4 - len(data) % 4) % 4
    data += b'\0' * padding
    
    result = ""
    for i in range(0, len(data), 4):
        val = int.from_bytes(data[i:i+4], 'big')
        chunk = ""
        for _ in range(5):
            val, rem = divmod(val, 85)
            chunk = ALPHABET[rem] + chunk
        result += chunk
    
    return result

def encode_base92(data: str) -> str:
    ALPHABET = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
               "[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    if isinstance(data, str): data = data.encode('utf-8')
    
    val = int.from_bytes(data.encode('utf-8'), 'big')
    res = []
    
    while val > 0:
        val, rem = divmod(val, 92)
        res.append(ALPHABET[rem])
        
    return "".join(reversed(res)) if res else ALPHABET[0]

def encode_hex(data: str) -> str:
    result = ""

    for letter in data:
        int_letter = ord(letter)
        result += hex(int_letter)[2:]

    return result

def encode_rot(data: str, offset: int) -> str:
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_UPPER = ALPHABET.upper()

    result = ""

    for letter in data:
        if letter in ALPHABET:
            result += ALPHABET[(ALPHABET.find(letter) + offset) % len(ALPHABET)]
        elif letter in ALPHABET_UPPER:
            result += ALPHABET_UPPER[(ALPHABET_UPPER.find(letter) + offset) % len(ALPHABET_UPPER)]
        else:
            result += letter

    return result

def encode_binary(data: str, spaces: bool) -> str:
    result = ""

    for letter in data:
        bin_letter = bin(ord(letter))[2:]
        result += "0" * (8 - len(bin_letter)) + bin_letter

        if spaces: result += " "

    if spaces:
        result = result[:-1]

    return result

def encode_morse(data: str) -> str:
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        '1': '.----', '2': '..--', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', '/': '-..-.', '-': '-....-',
        '(': '-.--.', ')': '-.--.-'
    }

    result = ""

    for letter in data:
        if letter.upper() in list(MORSE_CODE_DICT.keys()):
            result += MORSE_CODE_DICT[letter.upper()]
        else:
            result += letter

        result += " "

    result = result[:-1]

    return result

def encode_atbash(data: str) -> str:
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_UPPER = ALPHABET.upper()

    result = ""

    for letter in data:
        if letter in ALPHABET:
            result += ALPHABET[-ALPHABET.find(letter)-1]
        elif letter in ALPHABET_UPPER:
            result += ALPHABET_UPPER[-ALPHABET_UPPER.find(letter)-1]
        else:
            result += letter

    return result

def encode_url(data: str) -> str:
    SAFE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"
    
    result = ""
    for char in data:
        if char in SAFE_CHARS:
            result += char
        else:
            result += f"%{ord(char):02X}"
            
    return result
