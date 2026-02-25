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
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    padding = len(data) - len(data.lstrip(b'\0'))
    
    num = int.from_bytes(data, 'big')
    
    result = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        result = ALPHABET[remainder] + result
    
    return (ALPHABET[0] * padding) + result

def encode_base64(data):
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    
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

# === searchers ===

def default_search(text: list[str], search: str):
    text = "".join(text)

    return search in text

def default_reverse_search(text: list[str], search: str):
    text = "".join(text)

    return search[::-1] in text

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

def base58_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base58(search)
    search = search.replace("=", "")

    return search in text

def base58_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base58(search)
    search = search.replace("=", "")

    return search[::-1] in text

print(encode_base64("test"))