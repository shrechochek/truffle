from encoders import *
import core

# === searchers ===

# --- default

def default_search(text: list[str], search: str):
    text = "".join(text)

    print(text)

    return core.find_all_indices(text, search)

def default_reverse_search(text: list[str], search: str):
    text = "".join(text)

    return core.find_all_indices(text, search[::-1])

# --- base64

def base64_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base64(search)
    search = search.replace("=", "")

    return core.find_all_indices(text, search)

def base64_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base64(search)
    search = search.replace("=", "")

    return core.find_all_indices(text, search[::-1])

# --- base58

def base58_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base58(search)

    return core.find_all_indices(text, search)

def base58_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base58(search)

    return core.find_all_indices(text, search[::-1])

# --- base32

def base32_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base32(search)
    search = search.replace("=", "")

    return core.find_all_indices(text, search)

def base32_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base32(search)
    search = search.replace("=", "")

    return core.find_all_indices(text, search[::-1])

# --- base45

def base45_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base45(search)

    return core.find_all_indices(text, search)

def base45_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base45(search)

    return core.find_all_indices(text, search[::-1])

# --- base62

def base62_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base62(search)

    return core.find_all_indices(text, search)

def base62_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base62(search)

    return core.find_all_indices(text, search[::-1])

# --- base85

def base85_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base85(search)

    return core.find_all_indices(text, search)

def base85_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base85(search)

    return core.find_all_indices(text, search[::-1])

# --- base92

def base92_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base92(search)

    return core.find_all_indices(text, search)

def base92_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base92(search)

    return core.find_all_indices(text, search[::-1])

# --- hex

def hex_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_hex(search)

    return core.find_all_indices(text, search)

def hex_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_hex(search)

    return core.find_all_indices(text, search[::-1])

# --- rot

def rot_search(text: list[str], search: str, offset: int):
    text = "".join(text)
    search = encode_rot(search, offset)

    return core.find_all_indices(text, search)

def rot_reverse_search(text: list[str], search: str, offset: int):
    text = "".join(text)
    search = encode_rot(search, offset)

    return core.find_all_indices(text, search[::-1])

# --- binary

def binary_search(text: list[str], search: str, spaces: bool):
    text = "".join(text)
    search = encode_binary(search, spaces)

    return core.find_all_indices(text, search)

def binary_reverse_search(text: list[str], search: str, spaces: bool):
    text = "".join(text)
    search = encode_binary(search, spaces)

    return core.find_all_indices(text, search[::-1])

# --- morse

def morse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_morse(search)

    return core.find_all_indices(text, search)

def morse_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_morse(search)

    return core.find_all_indices(text, search[::-1])

# --- atbash

def atbash_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_atbash(search)

    return core.find_all_indices(text, search)

def atbash_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_atbash(search)

    return core.find_all_indices(text, search[::-1])

# --- url

def url_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_url(search)

    return core.find_all_indices(text, search)

def url_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_url(search)

    return core.find_all_indices(text, search[::-1])

strings = core.get_strings("example.png")

# print(encode_atbash("pico"))
print(default_reverse_search(strings, "uuu"))

# === finder ===

# def find_all():