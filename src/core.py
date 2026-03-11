import decoders
import encoders
import searchers
import re
import sys
import os
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

TERMINAL_SIZE = shutil.get_terminal_size(fallback=(80, 24))
STATUS_COLS = TERMINAL_SIZE.columns
STATUS_ROW = TERMINAL_SIZE.lines
STATUS_ENABLED = sys.stdout.isatty()
ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
BLIND_FLAG_PATTERN = re.compile(r'\{[^{}\r\n]+\}')
STATUS_VISIBLE = False

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
    ('no_decode', decoders.no_decode, None, False),
    ('no_decode_reverse', decoders.no_decode, None, True),
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
    if not STATUS_ENABLED:
        return

    global STATUS_VISIBLE

    sys.stdout.write("\r\033[2K")
    sys.stdout.write(_truncate_ansi_text(msg, max(1, STATUS_COLS - 1)))
    sys.stdout.flush()
    STATUS_VISIBLE = True


def clear_status():
    if not STATUS_ENABLED:
        return

    global STATUS_VISIBLE

    if not STATUS_VISIBLE:
        return

    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()
    STATUS_VISIBLE = False


def _format_progress(label: str, current: int, total: int, extra: str = "") -> str:
    total = max(total, 1)
    current = min(max(current, 0), total)
    percent = current / total
    bar_width = max(10, min(30, STATUS_COLS // 3))
    filled = int(bar_width * percent)
    bar = Colors.BG_GREEN + " " * filled + Colors.END + Colors.BG_RED + " " * (bar_width - filled) + Colors.END
    message = f"{Colors.CYAN}{label}{Colors.END} {bar} {Colors.GREEN}{current}{Colors.END}/{total} {percent * 100:5.1f}%"

    if extra:
        message = f"{message} {extra}"

    return message


def _truncate_ansi_text(text: str, max_visible_chars: int) -> str:
    visible_chars = 0
    position = 0
    result = []

    while position < len(text) and visible_chars < max_visible_chars:
        escape_match = ANSI_ESCAPE_PATTERN.match(text, position)
        if escape_match:
            result.append(escape_match.group(0))
            position = escape_match.end()
            continue

        result.append(text[position])
        visible_chars += 1
        position += 1

    truncated = ''.join(result)
    if '\033[' in truncated and not truncated.endswith(Colors.END):
        truncated += Colors.END

    return truncated

def get_strings(file_path, min_len=4):
    with open(file_path, "rb") as f:
        content = f.read()

    decoded_content = content.decode('utf-8', errors='ignore')
    result = []
    current_chars = []

    for char in decoded_content:
        if char.isprintable():
            current_chars.append(char)
            continue

        if len(current_chars) >= min_len:
            result.append(''.join(current_chars))
        current_chars = []

    if len(current_chars) >= min_len:
        result.append(''.join(current_chars))

    return result

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


def find_all(strings, search_text: str | None, max_depth: int = 1, enable_rot: bool = False, source_label: str | None = None, xor_key: str | None = None, progress_label: str | None = None, blind_mode: bool = False):
    if not strings:
        return 0

    plain_strings = "".join(strings)

    return _find_recursive(plain_strings, strings, search_text, max_depth, enable_rot, source_label, xor_key, progress_label, blind_mode)

def _find_recursive(plain_strings: str, strings: list[str], search_text: str | None, max_depth: int, enable_rot: bool, source_label: str | None = None, xor_key: str | None = None, progress_label: str | None = None, blind_mode: bool = False):
    if max_depth > 5 or (max_depth > 2 and enable_rot):
        clear_status()
        print(f"{Colors.BRIGHT_CYAN}Searching with depth {max_depth}... This may take a while.{Colors.END}\n")

    base_decoders = _get_base_decoders(enable_rot, xor_key)
    potential_encoded = _collect_potential_encoded(strings, plain_strings)
    found_results = set()  # remove duplicates
    total_candidates = len(potential_encoded)

    if progress_label and total_candidates > 0:
        status(_format_progress(progress_label, 0, total_candidates))

    update_interval = max(1, total_candidates // 100) if total_candidates > 0 else 1

    for index, encoded_text in enumerate(potential_encoded, start=1):
        _walk_decoder_chains(encoded_text, encoded_text, search_text, base_decoders, max_depth, [], found_results, source_label, blind_mode)

        if progress_label and (index == 1 or index == total_candidates or index % update_interval == 0):
            extra = f""
            if source_label:
                extra = f"{os.path.basename(source_label)} {extra}"
            status(_format_progress(progress_label, index, total_candidates, extra))

    if progress_label and total_candidates == 0:
        extra = f"{os.path.basename(source_label)} no-candidates" if source_label else "no-candidates"
        status(_format_progress(progress_label, 1, 1, extra))

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


def _walk_decoder_chains(original_text: str, current_text: str, search_text: str | None, base_decoders, depth_left: int, chain_names: list[str], found_results: set, source_label: str | None = None, blind_mode: bool = False):
    if depth_left == 0:
        return

    for name, decoder_func, param, is_reverse in base_decoders:
        if _should_skip_decoder(chain_names, name, param, is_reverse):
            continue

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

        match_text = _find_match_text(candidate, search_text, blind_mode)
        if match_text is not None:
            chain_str = " → ".join(chain_names)
            result_key = (chain_str, candidate[:100])
            if result_key not in found_results:
                found_results.add(result_key)
                _print_result({
                    'chain_str': chain_str,
                    'decoded': candidate,
                    'match_text': match_text,
                }, source_label)

        _walk_decoder_chains(original_text, candidate, search_text, base_decoders, depth_left - 1, chain_names, found_results, source_label, blind_mode)
        chain_names.pop()


def _find_match_text(text: str, search_text: str | None, blind_mode: bool) -> str | None:
    if search_text and search_text in text:
        return search_text

    if blind_mode:
        match = BLIND_FLAG_PATTERN.search(text)
        if match:
            return match.group(0)

    return None


def _get_decoder_family(name: str) -> str:
    if name.startswith('no_decode'):
        return 'identity'

    if name.startswith('rot'):
        return 'rot'

    if name.startswith('xor('):
        return 'xor'

    if name.startswith('atbash'):
        return 'atbash'

    if name.endswith('_reverse'):
        return name[:-8]

    return name


@lru_cache(maxsize=64)
def _is_single_byte_xor_key(key: str | None) -> bool:
    if key is None:
        return False

    if key.lower().startswith('0x'):
        try:
            return 0 <= int(key, 16) <= 0xFF
        except ValueError:
            return False

    return len(key.encode('utf-8')) == 1


def _should_skip_decoder(chain_names: list[str], name: str, param, is_reverse: bool) -> bool:
    if not chain_names:
        return False

    previous_name = chain_names[-1]
    previous_family = _get_decoder_family(previous_name)
    current_family = _get_decoder_family(name)

    if previous_family == 'rot' and current_family == 'rot':
        return True

    if previous_family == 'atbash' and current_family == 'atbash':
        return True

    if previous_family == 'identity' and current_family == 'identity':
        return True

    if previous_family == 'xor' and current_family == 'xor':
        previous_is_reverse = previous_name.endswith('_reverse')
        previous_base_name = previous_name[:-8] if previous_is_reverse else previous_name
        previous_key = previous_base_name[4:-1] if previous_base_name.startswith('xor(') else None
        if previous_key == param and not previous_is_reverse and not is_reverse:
            return True

        if previous_key == param and _is_single_byte_xor_key(param):
            return True

    return False


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

def _print_result(result, source_label: str | None = None):
    clear_status()

    if source_label:
        print(f"{Colors.BRIGHT_BLUE}File: {source_label}{Colors.END}")
    print(f"Found results for chain: {Colors.BRIGHT_YELLOW}{result['chain_str']}{Colors.END}")
    # print(f"{Colors.BLUE}Original text: {result['original'][:80]}{'...' if len(result['original']) > 80 else ''}{Colors.END}")
    # print(f"{Colors.BRIGHT_GREEN}Index: {result['index']}{Colors.END}")
    
    decoded = result['decoded']
    match_text = result['match_text']
    search_text_position = decoded.find(match_text)
    
    context_start = max(0, search_text_position - 50)
    context_end = min(len(decoded), search_text_position + len(match_text) + 50)
    context = decoded[context_start:context_end]
    
    highlight_pos = search_text_position - context_start
    print(f"{context[:highlight_pos]}{Colors.BOLD}{Colors.RED}{match_text}{Colors.END}{context[highlight_pos+len(match_text):]}")
    print()