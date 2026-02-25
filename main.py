import sys
from encoders import *
# from decoders import *
import decoders
import core

# === searchers ===

# --- default

def default_search(text: list[str], search: str):
    text = "".join(text)

    return core.find_all_indices(text, search)

def default_reverse_search(text: list[str], search: str):
    text = "".join(text)

    return core.find_all_indices(text, search[::-1])

# --- base64

def base64_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base64(search)
    search = search.replace("=", "")
    search = search[:-1] # cut for search improvement

    return core.find_all_indices(text, search)

def base64_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = encode_base64(search)
    search = search.replace("=", "")
    search = search[:-1] # cut for search improvement

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

searchers = [default_search, default_reverse_search, base64_search, base64_reverse_search, base58_search, base58_reverse_search,
             base32_search,  base32_reverse_search,  base45_search, base45_reverse_search, base62_search, base62_reverse_search,
             base85_search,  base85_reverse_search,  base92_search, base92_reverse_search, hex_search,    hex_reverse_search,
             rot_search,     rot_reverse_search,     binary_search, binary_reverse_search, morse_search,  morse_reverse_search,
             atbash_search,  atbash_reverse_search,  url_search,    url_reverse_search]

decoder_functions = [decoders.do_nothing,    decoders.decode_base64, decoders.decode_base58,
                     decoders.decode_base32, decoders.decode_base45, decoders.decode_base62,
                     decoders.decode_base85, decoders.decode_base92, decoders.decode_hex,
                     decoders.decode_rot,    decoders.decode_binary, decoders.decode_morse,
                     decoders.decode_atbash, decoders.decode_url]

sys_arguments = sys.argv[1:]
if len(sys_arguments) != 2:
    print(f"{core.Colors.BRIGHT_RED}incorrect number of arguments{core.Colors.END}")
    sys.exit(1)

file_name = sys_arguments[0]
strings = core.get_strings(file_name)
plain_strings = "".join(strings)

search_text = sys_arguments[1]

# === finder ===

def find_all():
    for i in range(len(searchers)):
        searcher = searchers[i]
        if searcher == rot_search or searcher == rot_reverse_search: # rot check
            for j in range(1,26):
                search_result = searcher(strings, search_text, j)

                if len(search_result) > 0:
                    print(f"Found results for {core.Colors.YELLOW}{str(searcher.__name__)}{core.Colors.END} {core.Colors.BLUE}offset = {str(j)}{core.Colors.END}")
                    for index in search_result:
                        print(f"{core.Colors.GREEN}index: {index}{core.Colors.END}") #plain_strings
                        text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                        if i % 2 == 1: # without reverse
                            text_cut = text_cut[::-1]

                        result = decode_rot(text_cut, j)
                        search_text_position = result.find(search_text)
                        print(f"{result[:search_text_position]}{core.Colors.RED}{search_text}{core.Colors.END}{result[search_text_position+len(search_text):]}")

        elif searcher == binary_search or searcher == binary_reverse_search:
            search_result = searcher(strings, search_text, True)

            if len(search_result) > 0:
                print(f"Found results for {core.Colors.YELLOW}{str(searcher.__name__)}{core.Colors.END} {core.Colors.BLUE}spaces = True{core.Colors.END}")
                for index in search_result:
                    print(f"{core.Colors.GREEN}index: {index}{core.Colors.END}") #plain_strings
                    text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                    if i % 2 == 1: # without reverse
                        text_cut = text_cut[::-1]

                    result = decoder_functions[(i)//2](text_cut)
                    search_text_position = result.find(search_text)
                    print(f"{result[:search_text_position]}{core.Colors.RED}{search_text}{core.Colors.END}{result[search_text_position+len(search_text):]}")

            search_result = searcher(strings, search_text, False)

            if len(search_result) > 0:
                print(f"Found results for {core.Colors.YELLOW}{str(searcher.__name__)}{core.Colors.END} {core.Colors.BLUE}spaces = False{core.Colors.END}")
                for index in search_result:
                    print(f"{core.Colors.GREEN}index: {index}{core.Colors.END}") #plain_strings
                    text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                    if i % 2 == 1: # without reverse
                        text_cut = text_cut[::-1]

                    result = decoder_functions[(i)//2](text_cut)
                    search_text_position = result.find(search_text)
                    print(f"{result[:search_text_position]}{core.Colors.RED}{search_text}{core.Colors.END}{result[search_text_position+len(search_text):]}")

        else:
            search_result = searcher(strings, search_text)
            if len(search_result) > 0:
                print(f"Found results for {core.Colors.YELLOW}{str(searcher.__name__)}{core.Colors.END}")
                for index in search_result:
                    print(f"{core.Colors.GREEN}index: {index}{core.Colors.END}") #plain_strings
                    text_cut = plain_strings[max(0, index-50):min(len(plain_strings), index+50)]
                    if i % 2 == 1: # without reverse
                        text_cut = text_cut[::-1]

                    result = decoder_functions[(i)//2](text_cut)
                    search_text_position = result.find(search_text)
                    print(f"{result[:search_text_position]}{core.Colors.RED}{search_text}{core.Colors.END}{result[search_text_position+len(search_text):]}")

print(core.pig_art)
find_all()