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


def find_all(strings, search_text: str):
    plain_strings =  "".join(strings)
    for i in range(len(searcher_functions)):
        searcher = searcher_functions[i]
        if searcher == searchers.rot_search or searcher == searchers.rot_reverse_search: # rot check
            for j in range(1,26):
                search_result = searcher(strings, search_text, j)

                if len(search_result) > 0:
                    print(f"Found results for {Colors.YELLOW}{str(searcher.__name__)}{Colors.END} {Colors.BLUE}offset = {str(j)}{Colors.END}")
                    for index in search_result:
                        print(f"{Colors.GREEN}index: {index}{Colors.END}") #plain_strings
                        text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                        if i % 2 == 1: # without reverse
                            text_cut = text_cut[::-1]

                        result = decoders.decode_rot(text_cut, j)
                        search_text_position = result.find(search_text)
                        print(f"{result[:search_text_position]}{Colors.RED}{search_text}{Colors.END}{result[search_text_position+len(search_text):]}")

        elif searcher == searchers.binary_search or searcher == searchers.binary_reverse_search:
            search_result = searcher(strings, search_text, True)

            if len(search_result) > 0:
                print(f"Found results for {Colors.YELLOW}{str(searcher.__name__)}{Colors.END} {Colors.BLUE}spaces = True{Colors.END}")
                for index in search_result:
                    print(f"{Colors.GREEN}index: {index}{Colors.END}") #plain_strings
                    text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                    if i % 2 == 1: # without reverse
                        text_cut = text_cut[::-1]

                    result = decoder_functions[(i)//2](text_cut)
                    search_text_position = result.find(search_text)
                    print(f"{result[:search_text_position]}{Colors.RED}{search_text}{Colors.END}{result[search_text_position+len(search_text):]}")

            search_result = searcher(strings, search_text, False)

            if len(search_result) > 0:
                print(f"Found results for {Colors.YELLOW}{str(searcher.__name__)}{Colors.END} {Colors.BLUE}spaces = False{Colors.END}")
                for index in search_result:
                    print(f"{Colors.GREEN}index: {index}{Colors.END}") #plain_strings
                    text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                    if i % 2 == 1: # without reverse
                        text_cut = text_cut[::-1]

                    result = decoder_functions[(i)//2](text_cut)
                    search_text_position = result.find(search_text)
                    print(f"{result[:search_text_position]}{Colors.RED}{search_text}{Colors.END}{result[search_text_position+len(search_text):]}")

        else:
            search_result = searcher(strings, search_text)
            if len(search_result) > 0:
                print(f"Found results for {Colors.YELLOW}{str(searcher.__name__)}{Colors.END}")
                for index in search_result:
                    print(f"{Colors.GREEN}index: {index}{Colors.END}") #plain_strings
                    text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                    if i % 2 == 1: # without reverse
                        text_cut = text_cut[::-1]

                    result = decoder_functions[(i)//2](text_cut)
                    search_text_position = result.find(search_text)
                    print(f"{result[:search_text_position]}{Colors.RED}{search_text}{Colors.END}{result[search_text_position+len(search_text):]}")
