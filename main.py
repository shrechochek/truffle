from encoders import *
import string

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

# --- hex

def hex_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_hex(search)

    return search in text

def hex_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_hex(search)

    return search[::-1] in text

# --- rot

def rot_search(text: list[str], search: str, offset: int):
    text = "".join(text)
    search = encode_rot(search, offset)

    return search in text

def rot_reverse_search(text: list[str], search: str, offset: int):
    text = "".join(text)
    search = encode_rot(search, offset)

    return search[::-1] in text

# --- binary

def binary_search(text: list[str], search: str, spaces: bool):
    text = "".join(text)
    search = encode_binary(search, spaces)

    return search in text

def binary_reverse_search(text: list[str], search: str, spaces: bool):
    text = "".join(text)
    search = encode_binary(search, spaces)

    return search[::-1] in text

# --- morse

def morse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_morse(search)

    return search in text

def morse_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_morse(search)

    return search[::-1] in text

# --- atbash

def atbash_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_atbash(search)

    return search in text

def atbash_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_atbash(search)

    return search[::-1] in text

# --- url

def url_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_url(search)

    return search in text

def url_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_url(search)

    return search[::-1] in text

print(encode_atbash("pico"))