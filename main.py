import string

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

def classic_search(strings: list[str], search: str):
    string = "".join(strings)
    print(string)
    return search in string

print(classic_search(strings, "b"))