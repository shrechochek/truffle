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