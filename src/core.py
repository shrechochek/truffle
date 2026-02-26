import decoders
import encoders
import searchers
import sys

pig_art = r'''
                                                                  ⣀⣤⣤⣶⣶⣶⣶⣦⣤⣄⣀           
  _______ _____  _    _ ______ ______ _      ______       ⢀⡶⢻⡦⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣴⣾⡿ ⣠ 
 |__   __|  __ \| |  | |  ____|  ____| |    |  ____|      ⠠⣬⣷⣾⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣌⣋⣉⣄⠘⠋  
    | |  | |__) | |  | | |__  | |__  | |    | |__           ⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡄    
    | |  |  _  /| |  | |  __| |  __| | |    |  __|          ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣷⣶⡄ 
    | |  | | \ \| |__| | |    | |    | |____| |____         ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇ 
    |_|  |_|  \_\\____/|_|    |_|    |______|______|        ⠸⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠻⠿⣿⣿⡿⠛⠛⠛⠋⠉⠉   
                                                             ⢻⣿⣿  ⢸⣿⡇     ⢻⣿⠃⠸⣿⡇      
                                                             ⠈⠿⠇   ⠻⠇     ⠈⠿  ⠻⠿
'''

class Colors:
    END = '\033[0m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
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

def get_strings(file_path, min_len=4):
    with open(file_path, "rb") as f:
        content = f.read()
    printable_bytes = set(range(32, 127)) 
    
    result = []
    current_str = bytearray()
    
    for byte in content:
        if byte in printable_bytes:
            current_str.append(byte)
        else:
            if len(current_str) >= min_len:
                result.append(current_str.decode('ascii', errors='ignore'))
            current_str = bytearray()

    if len(current_str) >= min_len:
        result.append(current_str.decode('ascii', errors='ignore'))
            
    return result

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
             searchers.atbash_search,  searchers.atbash_reverse_search,  searchers.url_search,    searchers.url_reverse_search]

decoder_functions = [decoders.no_decode,    decoders.decode_base64, decoders.decode_base58,
                     decoders.decode_base32, decoders.decode_base45, decoders.decode_base62,
                     decoders.decode_base85, decoders.decode_base92, decoders.decode_hex,
                     decoders.decode_rot,    decoders.decode_binary, decoders.decode_morse,
                     decoders.decode_atbash, decoders.decode_url]


def find_all(strings, search_text: str, max_depth: int = 1, enable_rot: bool = True):
    plain_strings = "".join(strings)
    
    if max_depth == 1:
        # Оригинальная логика для глубины 1
        _find_depth_one(plain_strings, strings, search_text, enable_rot)
    else:
        # Рекурсивный поиск для глубины > 1
        _find_recursive(plain_strings, strings, search_text, max_depth, enable_rot)


def _find_depth_one(plain_strings: str, strings: list[str], search_text: str, enable_rot: bool):
    """Оригинальная логика поиска на глубине 1"""
    for i in range(len(searcher_functions)):
        searcher = searcher_functions[i]
        
        if searcher == searchers.rot_search or searcher == searchers.rot_reverse_search:
            if not enable_rot:
                continue
                
            for j in range(1, 26):
                search_result = searcher(strings, search_text, j)
                if len(search_result) > 0:
                    print(f"Found results for {Colors.YELLOW}{str(searcher.__name__)}{Colors.END} {Colors.BLUE}offset = {str(j)}{Colors.END}")
                    for index in search_result:
                        print(f"{Colors.GREEN}index: {index}{Colors.END}")
                        text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                        if i % 2 == 1:
                            text_cut = text_cut[::-1]
                        result = decoders.decode_rot(text_cut, j)
                        search_text_position = result.find(search_text)
                        print(f"{result[:search_text_position]}{Colors.RED}{search_text}{Colors.END}{result[search_text_position+len(search_text):]}")

        elif searcher == searchers.binary_search or searcher == searchers.binary_reverse_search:
            for spaces in [True, False]:
                search_result = searcher(strings, search_text, spaces)
                if len(search_result) > 0:
                    print(f"Found results for {Colors.YELLOW}{str(searcher.__name__)}{Colors.END} {Colors.BLUE}spaces = {spaces}{Colors.END}")
                    for index in search_result:
                        print(f"{Colors.GREEN}index: {index}{Colors.END}")
                        text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                        if i % 2 == 1:
                            text_cut = text_cut[::-1]
                        result = decoder_functions[(i)//2](text_cut)
                        search_text_position = result.find(search_text)
                        print(f"{result[:search_text_position]}{Colors.RED}{search_text}{Colors.END}{result[search_text_position+len(search_text):]}")

        else:
            search_result = searcher(strings, search_text)
            if len(search_result) > 0:
                print(f"Found results for {Colors.YELLOW}{str(searcher.__name__)}{Colors.END}")
                for index in search_result:
                    print(f"{Colors.GREEN}index: {index}{Colors.END}")
                    text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                    if i % 2 == 1:
                        text_cut = text_cut[::-1]
                    result = decoder_functions[(i)//2](text_cut)
                    search_text_position = result.find(search_text)
                    print(f"{result[:search_text_position]}{Colors.RED}{search_text}{Colors.END}{result[search_text_position+len(search_text):]}")


def _find_recursive(plain_strings: str, strings: list[str], search_text: str, max_depth: int, enable_rot: bool):
    """Рекурсивный поиск с заданной глубиной"""
    print(f"{Colors.CYAN}Searching with depth {max_depth}... This may take a while.{Colors.END}\n")
    
    # generating all possible chains of combinations
    chains = _generate_decoder_chains(max_depth, enable_rot)
    
    import re
    potential_encoded = []
    
    for string in strings:
        matches = re.findall(r'[A-Za-z0-9+/=\-_.~%:$#@!*]+', string)
        potential_encoded.extend(matches)
        potential_encoded.append(string.strip())
    
    for i in range(0, len(plain_strings), 30):
        potential_encoded.append(plain_strings[i:min(i+150, len(plain_strings))])
    
    potential_encoded = list(set([s.strip() for s in potential_encoded if len(s.strip()) >= 4]))
    
    found_results = set()  # remove duplicates
    
    for encoded_text in potential_encoded:
        for chain in chains:
            result = _try_decode_chain(encoded_text, search_text, chain)
            if result:
                result_key = (result['chain_str'], result['decoded'][:100])
                if result_key not in found_results:
                    found_results.add(result_key)
                    _print_result(result, search_text)


def _generate_decoder_chains(depth: int, enable_rot: bool):
    # genearte all possible chaings
    base_decoders = [
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
    
    # rot
    if enable_rot:
        for offset in range(1, 26):
            base_decoders.append((f'rot{offset}', decoders.decode_rot, offset, False))
            base_decoders.append((f'rot{offset}_reverse', decoders.decode_rot, offset, True))
    
    if depth == 1:
        return [[decoder] for decoder in base_decoders]
    
    chains = []
    
    def generate(current_chain, remaining_depth):
        if remaining_depth == 0:
            chains.append(current_chain[:])
            return
        
        for decoder in base_decoders:
            current_chain.append(decoder)
            generate(current_chain, remaining_depth - 1)
            current_chain.pop()
    
    generate([], depth)
    return chains


def _can_be_encoding(text: str, encoding_name: str) -> bool:
    if not text:
        return False
    
    if 'url' in encoding_name.lower():
        return '%' in text and any(c in '0123456789ABCDEFabcdef' for c in text)
    
    if 'morse' in encoding_name.lower():
        morse_chars = set('.-')
        return any(c in morse_chars for c in text) and not any(c.isalnum() for c in text.replace(' ', ''))
    
    if 'binary' in encoding_name.lower():
        binary_chars = set('01 ')
        return len(text) >= 8 and all(c in binary_chars for c in text)
    
    if 'hex' in encoding_name.lower():
        hex_chars = set('0123456789ABCDEFabcdef')
        return len(text) >= 2 and all(c in hex_chars for c in text)
    
    if 'base64' in encoding_name.lower():
        base64_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
        return len(text) >= 4 and all(c in base64_chars for c in text)
    
    if 'base58' in encoding_name.lower():
        forbidden = set('0OIl')
        return not any(c in forbidden for c in text) and text.isalnum()
    
    if 'base32' in encoding_name.lower():
        base32_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=')
        return len(text) >= 4 and all(c in base32_chars for c in text.upper())
    
    if 'base45' in encoding_name.lower():
        base45_chars = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:')
        return all(c in base45_chars for c in text.upper())
    
    if 'base62' in encoding_name.lower():
        return text.isalnum() and len(text) >= 4
    
    if 'base85' in encoding_name.lower():
        return len(text) >= 5 and any(c in '.-:+=^!/*?&<>()[]{}@%$#' for c in text)
    
    if 'base92' in encoding_name.lower():
        return len(text) >= 4 and any(c in '!#$%&\'()*+,-./:;<=>?@[]^_`{|}~' for c in text)
    
    if 'rot' in encoding_name.lower():
        return any(c.isalpha() for c in text)
    
    if 'atbash' in encoding_name.lower():
        return any(c.isalpha() for c in text)
    
    if 'no_decode' in encoding_name.lower():
        return True
    
    return True


def _try_decode_chain(text: str, search_text: str, chain):
    decoded = text
    chain_names = []
    
    for name, decoder_func, param, is_reverse in chain:
        if not _can_be_encoding(decoded, name):
            return None
        
        if is_reverse:
            decoded = decoded[::-1]
        
        try:
            if param is not None:
                decoded = decoder_func(decoded, param)
            else:
                decoded = decoder_func(decoded)
        except Exception:
            return None
        
        chain_names.append(name)
        
        if not decoded or len(decoded) == 0:
            return None
    
    if search_text in decoded:
        return {
            'chain_str': " → ".join(chain_names),
            'decoded': decoded,
            'original': text
        }
    
    return None


def _print_result(result, search_text):
    print(f"Found results for chain: {Colors.YELLOW}{result['chain_str']}{Colors.END}")
    print(f"{Colors.BLUE}Original text: {result['original'][:80]}{'...' if len(result['original']) > 80 else ''}{Colors.END}")
    
    decoded = result['decoded']
    search_text_position = decoded.find(search_text)
    
    context_start = max(0, search_text_position - 50)
    context_end = min(len(decoded), search_text_position + len(search_text) + 50)
    context = decoded[context_start:context_end]
    
    highlight_pos = search_text_position - context_start
    print(f"{context[:highlight_pos]}{Colors.RED}{search_text}{Colors.END}{context[highlight_pos+len(search_text):]}")
    print()
