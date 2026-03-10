import encoders
import core

# === searchers ===

def _normalize_text(text: str | list[str]) -> str:
    return text if isinstance(text, str) else "".join(text)


def _search(text: str | list[str], search: str):
    return core.find_all_indices(_normalize_text(text), search)


def _encoded_search(text: str | list[str], search: str, encoder, reverse: bool = False, strip_equals: bool = False, trim_last: bool = False, *encoder_args):
    encoded = encoder(search, *encoder_args)

    if strip_equals:
        encoded = encoded.replace("=", "")

    if trim_last and encoded:
        encoded = encoded[:-1]

    if reverse:
        encoded = encoded[::-1]

    return _search(text, encoded)

# --- default

def default_search(text: list[str], search: str):
    return _search(text, search)

def default_reverse_search(text: list[str], search: str):
    return _search(text, search[::-1])

# --- base64

def base64_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base64, False, True, True)

def base64_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base64, True, True, True)

# --- base58

def base58_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base58)

def base58_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base58, True)

# --- base32

def base32_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base32, False, True)

def base32_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base32, True, True)

# --- base45

def base45_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base45)

def base45_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base45, True)

# --- base62

def base62_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base62)

def base62_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base62, True)

# --- base85

def base85_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base85)

def base85_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base85, True)

# --- base92

def base92_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base92)

def base92_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_base92, True)

# --- hex

def hex_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_hex)

def hex_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_hex, True)

# --- rot

def rot_search(text: list[str], search: str, offset: int):
    return _encoded_search(text, search, encoders.encode_rot, False, False, False, offset)

def rot_reverse_search(text: list[str], search: str, offset: int):
    return _encoded_search(text, search, encoders.encode_rot, True, False, False, offset)

# --- binary

def binary_search(text: list[str], search: str, spaces: bool):
    return _encoded_search(text, search, encoders.encode_binary, False, False, False, spaces)

def binary_reverse_search(text: list[str], search: str, spaces: bool):
    return _encoded_search(text, search, encoders.encode_binary, True, False, False, spaces)

# --- morse

def morse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_morse)

def morse_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_morse, True)

# --- atbash

def atbash_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_atbash)

def atbash_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_atbash, True)

# --- url

def url_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_url)

def url_reverse_search(text: list[str], search: str):
    return _encoded_search(text, search, encoders.encode_url, True)

# --- xor

def xor_search(text: list[str], search: str, key: int | str):
    return _encoded_search(text, search, encoders.encode_xor, False, False, False, key)

def xor_reverse_search(text: list[str], search: str, key: int | str):
    return _encoded_search(text, search, encoders.encode_xor, True, False, False, key)
