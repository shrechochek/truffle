import string
import base64

# === strings function ===

def get_strings(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    
    printable_bytes = string.printable.encode('ascii')
    
    result = []
    current_str = b""
    
    for byte in content:
        if byte in printable_bytes:
            current_str += bytes([byte])
        else:
            if len(current_str) > 0:
                result.append(current_str.decode('ascii', errors='ignore'))
            current_str = b""
            
    return result

strings = get_strings("example.png")

# === encoders ===

def encode_base58(data):
    ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    if isinstance(data, str): data = data.encode('utf-8')
    padding = len(data) - len(data.lstrip(b'\0'))
    
    num = int.from_bytes(data, 'big')
    
    result = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        result = ALPHABET[remainder] + result
    
    return (ALPHABET[0] * padding) + result

def encode_base64(data):
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

def encode_base32(data):
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

def encode_base45(data):
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

def encode_base62(data):
    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if isinstance(data, str): data = data.encode('utf-8')
    
    num = int.from_bytes(data, 'big')
    if num == 0: return ALPHABET[0]
    
    result = ""
    while num > 0:
        num, rem = divmod(num, 62)
        result = ALPHABET[rem] + result

    return result

def encode_base85(data):
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

def encode_base92(text):
    ALPHABET = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
               "[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    if isinstance(data, str): data = data.encode('utf-8')
    
    val = int.from_bytes(text.encode('utf-8'), 'big')
    res = []
    
    while val > 0:
        val, rem = divmod(val, 92)
        res.append(ALPHABET[rem])
        
    return "".join(reversed(res)) if res else ALPHABET[0]

# === searchers ===

# --- default

def default_search(text: list[str], search: str):
    text = "".join(text)

    return search in text

def default_reverse_search(text: list[str], search: str):
    text = "".join(text)

    return search[::-1] in text

# --- base64

def base64_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base64(search)
    search = search.replace("=", "")

    return search in text

def base64_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base64(search)
    search = search.replace("=", "")

    return search[::-1] in text

# --- base58

def base58_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base58(search)

    return search in text

def base58_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base58(search)

    return search[::-1] in text

# --- base32

def base32_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base32(search)
    search = search.replace("=", "")

    return search in text

def base32_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base32(search)
    search = search.replace("=", "")

    return search[::-1] in text

# --- base45

def base45_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base45(search)

    return search in text

def base45_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base45(search)

    return search[::-1] in text

# --- base62

def base62_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base62(search)

    return search in text

def base62_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base62(search)

    return search[::-1] in text

# --- base85

def base85_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base85(search)

    return search in text

def base85_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base85(search)

    return search[::-1] in text

# --- base92

def base92_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base92(search)

    return search in text

def base92_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base92(search)

    return search[::-1] in text

print(encode_base64("test"))