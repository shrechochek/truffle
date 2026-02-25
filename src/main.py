import sys
import core

sys_arguments = sys.argv[1:]
if len(sys_arguments) != 2:
    print(f"{core.Colors.BRIGHT_RED}incorrect number of arguments{core.Colors.END}")
    sys.exit(1)

file_name = sys_arguments[0]
strings = core.get_strings(file_name)

search_text = sys_arguments[1]

print(core.pig_art)
core.find_all(strings, search_text)