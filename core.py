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