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

# === searchers ===

def default_search(text: list[str], search: str):
    text = "".join(text)
    return search in text

def default_reverse_search(text: list[str], search: str):
    text = "".join(text)
    return search[::-1] in text

def base64_search(text: list[str], search: str):
    text = "".join(text)
    search = search.encode("utf-8")
    search = base64.b64encode(search)
    search = search.decode("ascii")
    search = search.replace("=", "")

    return search in text

def base64_reverse_search(text: list[str], search: str):
    text = "".join(text)
    search = search.encode("utf-8")
    search = base64.b64encode(search)
    search = search.decode("ascii")
    search = search.replace("=", "")

    return search in text




print(base64_search(strings, "b"))