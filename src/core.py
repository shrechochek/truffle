import decoders
import encoders
import searchers
import re
import sys
from functools import lru_cache
from itertools import zip_longest
import shutil

pig_art = r'''
          ⣀⣤⣤⣶⣶⣶⣶⣦⣤⣄⣀           
 ⢀⡶⢻⡦⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣴⣾⡿ ⣠ 
 ⠠⣬⣷⣾⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣌⣋⣉⣄⠘⠋  
   ⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡄    
   ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣷⣶⡄ 
   ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇ 
   ⠸⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠻⠿⣿⣿⡿⠛⠛⠛⠋⠉⠉   
    ⢻⣿⣿  ⢸⣿⡇     ⢻⣿⠃⠸⣿⡇      
    ⠈⠿⠇   ⠻⠇     ⠈⠿  ⠻⠿
'''

main_text = r'''
  _______ _____  _    _ ______ ______ _      ______ 
 |__   __|  __ \| |  | |  ____|  ____| |    |  ____|
    | |  | |__) | |  | | |__  | |__  | |    | |__   
    | |  |  _  /| |  | |  __| |  __| | |    |  __|   
    | |  | | \ \| |__| | |    | |    | |____| |____  
    |_|  |_|  \_\\____/|_|    |_|    |______|______|   
'''

main_text_and_pig_art = r'''
                                                              ⣀⣤⣤⣶⣶⣶⣶⣦⣤⣄⣀           
  _______ _____  _    _ ______ ______ _      ______  ⢀⡶⢻⡦⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣴⣾⡿ ⣠ 
 |__   __|  __ \| |  | |  ____|  ____| |    |  ____| ⠠⣬⣷⣾⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣌⣋⣉⣄⠘⠋  
    | |  | |__) | |  | | |__  | |__  | |    | |__      ⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡄    
    | |  |  _  /| |  | |  __| |  __| | |    |  __|     ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣷⣶⡄ 
    | |  | | \ \| |__| | |    | |    | |____| |____    ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇ 
    |_|  |_|  \_\\____/|_|    |_|    |______|______|   ⠸⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠻⠿⣿⣿⡿⠛⠛⠛⠋⠉⠉   
                                                        ⢻⣿⣿  ⢸⣿⡇     ⢻⣿⠃⠸⣿⡇      
                                                        ⠈⠿⠇   ⠻⠇     ⠈⠿  ⠻⠿
'''

STATUS_ROW, cols = shutil.get_terminal_size(fallback=(80, 24))

PRINTABLE_ASCII_PATTERN = re.compile(rb'[\x20-\x7e]{4,}')
POTENTIAL_ENCODED_PATTERN = re.compile(r'[A-Za-z0-9+/=\-_.~%:$#@!*]+')

MORSE_CHARS = frozenset('.-')
BINARY_CHARS = frozenset('01 ')
HEX_CHARS = frozenset('0123456789ABCDEFabcdef')
BASE64_CHARS = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
BASE32_CHARS = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=')
BASE45_CHARS = frozenset('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:')
BASE58_FORBIDDEN = frozenset('0OIl')
BASE85_SPECIAL_CHARS = frozenset('.-:+=^!/*?&<>()[]{}@%$#')
BASE92_SPECIAL_CHARS = frozenset("!#$%&'()*+,-./:;<=>?@[]^_`{|}~")

BASE_DECODERS = [
    ('no_decode', decoders.no_decode, None, False),
    ('base64', decoders.decode_base64, None, False),
    ('base64_reverse', decoders.decode_base64, None, True),
    ('base58', decoders.decode_base58, None, False),
    ('base58_reverse', decoders.decode_base58, None, True),
    ('base32', decoders.decode_base32, None, False),
    ('base32_reverse', decoders.decode_base32, None, True),
    ('base45', decoders.decode_base45, None, False),
    ('base45_reverse', decoders.decode_base45, None, True),
    ('base62', decoders.decode_base62, None, False),
    ('base62_reverse', decoders.decode_base62, None, True),
    ('base85', decoders.decode_base85, None, False),
    ('base85_reverse', decoders.decode_base85, None, True),
    ('base92', decoders.decode_base92, None, False),
    ('base92_reverse', decoders.decode_base92, None, True),
    ('hex', decoders.decode_hex, None, False),
    ('hex_reverse', decoders.decode_hex, None, True),
    ('binary', decoders.decode_binary, None, False),
    ('binary_reverse', decoders.decode_binary, None, True),
    ('morse', decoders.decode_morse, None, False),
    ('morse_reverse', decoders.decode_morse, None, True),
    ('atbash', decoders.decode_atbash, None, False),
    ('atbash_reverse', decoders.decode_atbash, None, True),
    ('url', decoders.decode_url, None, False),
    ('url_reverse', decoders.decode_url, None, True),
]

class Colors:
    END = '\033[0m'
    
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    STRIKETHROUGH = '\033[9m'
    REVERSE = '\033[7m'
    INVISIBLE = '\033[8m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

def status(msg):
    sys.stdout.write(f"\0337")
    sys.stdout.write(f"\033[{STATUS_ROW};1H")
    sys.stdout.write("\033[2K")
    sys.stdout.write(msg[:cols])
    sys.stdout.write("\0338")
    sys.stdout.flush()

def get_strings(file_path, min_len=4):
    with open(file_path, "rb") as f:
        content = f.read()

    if min_len <= 4:
        matches = PRINTABLE_ASCII_PATTERN.findall(content)
    else:
        pattern = rb'[\x20-\x7e]{' + str(min_len).encode('ascii') + rb',}'
        matches = re.findall(pattern, content)

    return [match.decode('ascii') for match in matches]

def get_vertical_strings(text: list[str]):
    if not text:
        return []

    return ["".join(column) for column in zip_longest(*text, fillvalue="")]

def find_all_indices(text: str, substring: str) -> str:
    indices = []
    start = 0
    
    while True:
        index = text.find(substring, start)
        
        if index == -1:
            break
            
        indices.append(index)
        start = index + 1
        
    return indices

searcher_functions = [searchers.default_search, searchers.default_reverse_search, searchers.base64_search, searchers.base64_reverse_search, searchers.base58_search, searchers.base58_reverse_search,
                      searchers.base32_search,  searchers.base32_reverse_search,  searchers.base45_search, searchers.base45_reverse_search, searchers.base62_search, searchers.base62_reverse_search,
                      searchers.base85_search,  searchers.base85_reverse_search,  searchers.base92_search, searchers.base92_reverse_search, searchers.hex_search,    searchers.hex_reverse_search,
                      searchers.rot_search,     searchers.rot_reverse_search,     searchers.binary_search, searchers.binary_reverse_search, searchers.morse_search,  searchers.morse_reverse_search,
                      searchers.atbash_search,  searchers.atbash_reverse_search,  searchers.url_search,    searchers.url_reverse_search,
                      searchers.xor_search,     searchers.xor_reverse_search]

decoder_functions = [decoders.no_decode,     decoders.decode_base64, decoders.decode_base58,
                     decoders.decode_base32, decoders.decode_base45, decoders.decode_base62,
                     decoders.decode_base85, decoders.decode_base92, decoders.decode_hex,
                     decoders.decode_rot,    decoders.decode_binary, decoders.decode_morse,
                     decoders.decode_atbash, decoders.decode_url, decoders.decode_xor]


def find_all(strings, search_text: str, max_depth: int = 1, enable_rot: bool = False, source_label: str | None = None, xor_key: str | None = None):
    if not strings:
        return 0

    plain_strings = "".join(strings)

    return _find_recursive(plain_strings, strings, search_text, max_depth, enable_rot, source_label, xor_key)

def _find_recursive(plain_strings: str, strings: list[str], search_text: str, max_depth: int, enable_rot: bool, source_label: str | None = None, xor_key: str | None = None):
    if max_depth > 5 or (max_depth > 2 and enable_rot is not None):
        print(f"{Colors.BRIGHT_CYAN}Searching with depth {max_depth}... This may take a while.{Colors.END}\n")

    base_decoders = _get_base_decoders(enable_rot, xor_key)
    potential_encoded = _collect_potential_encoded(strings, plain_strings)
    found_results = set()  # remove duplicates

    for encoded_text in potential_encoded:
        _walk_decoder_chains(encoded_text, encoded_text, search_text, base_decoders, max_depth, [], found_results, source_label)

    return len(found_results)


def _get_base_decoders(enable_rot: bool, xor_key: str | None = None):
    base_decoders = list(BASE_DECODERS)

    if enable_rot:
        for offset in range(1, 26):
            base_decoders.append((f'rot{offset}', decoders.decode_rot, offset, False))
            base_decoders.append((f'rot{offset}_reverse', decoders.decode_rot, offset, True))

    if xor_key is not None:
        base_decoders.append((f'xor({xor_key})', decoders.decode_xor, xor_key, False))
        base_decoders.append((f'xor({xor_key})_reverse', decoders.decode_xor, xor_key, True))

    return base_decoders


def _collect_potential_encoded(strings: list[str], plain_strings: str):
    potential_encoded = set()

    for string in strings:
        stripped = string.strip()
        if len(stripped) >= 4:
            potential_encoded.add(stripped)

        for match in POTENTIAL_ENCODED_PATTERN.findall(string):
            stripped_match = match.strip()
            if len(stripped_match) >= 4:
                potential_encoded.add(stripped_match)

    for i in range(0, len(plain_strings), 30):
        chunk = plain_strings[i:min(i + 150, len(plain_strings))].strip()
        if len(chunk) >= 4:
            potential_encoded.add(chunk)

    return potential_encoded


def _walk_decoder_chains(original_text: str, current_text: str, search_text: str, base_decoders, depth_left: int, chain_names: list[str], found_results: set, source_label: str | None = None):
    if depth_left == 0:
        if search_text in current_text:
            chain_str = " → ".join(chain_names)
            result_key = (chain_str, current_text[:100])
            if result_key not in found_results:
                found_results.add(result_key)
                _print_result({
                    # 'index': original_text.index(current_text),
                    'chain_str': chain_str,
                    'decoded': current_text,
                    # 'original': original_text,
                }, search_text, source_label)
        return

    for name, decoder_func, param, is_reverse in base_decoders:
        if not _can_be_encoding(current_text, name):
            continue

        candidate = current_text[::-1] if is_reverse else current_text

        try:
            if param is not None:
                candidate = decoder_func(candidate, param)
            else:
                candidate = decoder_func(candidate)
        except Exception:
            continue

        if not candidate:
            continue

        chain_names.append(name)
        _walk_decoder_chains(original_text, candidate, search_text, base_decoders, depth_left - 1, chain_names, found_results, source_label)
        chain_names.pop()


@lru_cache(maxsize=16384)
def _can_be_encoding(text: str, encoding_name: str) -> bool:
    if not text:
        return False
    
    if 'url' in encoding_name.lower():
        return '%' in text and any(c in HEX_CHARS for c in text)
    
    if 'morse' in encoding_name.lower():
        return any(c in MORSE_CHARS for c in text) and not any(c.isalnum() for c in text.replace(' ', ''))
    
    if 'binary' in encoding_name.lower():
        return len(text) >= 8 and all(c in BINARY_CHARS for c in text)
    
    if 'hex' in encoding_name.lower():
        return len(text) >= 2 and all(c in HEX_CHARS for c in text)
    
    if 'base64' in encoding_name.lower():
        return len(text) >= 4 and all(c in BASE64_CHARS for c in text)
    
    if 'base58' in encoding_name.lower():
        return not any(c in BASE58_FORBIDDEN for c in text) and text.isalnum()
    
    if 'base32' in encoding_name.lower():
        return len(text) >= 4 and all(c in BASE32_CHARS for c in text.upper())
    
    if 'base45' in encoding_name.lower():
        return all(c in BASE45_CHARS for c in text.upper())
    
    if 'base62' in encoding_name.lower():
        return text.isalnum() and len(text) >= 4
    
    if 'base85' in encoding_name.lower():
        return len(text) >= 5 and any(c in BASE85_SPECIAL_CHARS for c in text)
    
    if 'base92' in encoding_name.lower():
        return len(text) >= 4 and any(c in BASE92_SPECIAL_CHARS for c in text)
    
    if 'rot' in encoding_name.lower():
        return any(c.isalpha() for c in text)

    if 'xor' in encoding_name.lower():
        return True
    
    if 'atbash' in encoding_name.lower():
        return any(c.isalpha() for c in text)
    
    if 'no_decode' in encoding_name.lower():
        return True
    
    return True

def _print_result(result, search_text, source_label: str | None = None):
    if source_label:
        print(f"{Colors.BRIGHT_BLUE}File: {source_label}{Colors.END}")
    print(f"Found results for chain: {Colors.BRIGHT_YELLOW}{result['chain_str']}{Colors.END}")
    # print(f"{Colors.BLUE}Original text: {result['original'][:80]}{'...' if len(result['original']) > 80 else ''}{Colors.END}")
    # print(f"{Colors.BRIGHT_GREEN}Index: {result['index']}{Colors.END}")
    
    decoded = result['decoded']
    search_text_position = decoded.find(search_text)
    
    context_start = max(0, search_text_position - 50)
    context_end = min(len(decoded), search_text_position + len(search_text) + 50)
    context = decoded[context_start:context_end]
    
    highlight_pos = search_text_position - context_start
    print(f"{context[:highlight_pos]}{Colors.BOLD}{Colors.RED}{search_text}{Colors.END}{context[highlight_pos+len(search_text):]}")
    print()