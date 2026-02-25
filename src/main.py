import sys
import core
import argparse

parser = argparse.ArgumentParser(description="CTF: String Searcher")
parser.add_argument("file_name", help="Path to the file to search")
parser.add_argument("search", help="Text to search for in the file")
parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive search (search inside decoded results)")

args = parser.parse_args()

#sys_arguments = sys.argv[1:]
#if len(sys_arguments) != 2:
#    print(f"{core.Colors.BRIGHT_RED}incorrect number of arguments{core.Colors.END}")
#    sys.exit(1)

file_name = args.file_name
search_text = args.search
recursive = args.recursive

strings = core.get_strings(file_name)


print(core.pig_art)
core.find_all(strings, search_text, recursive=recursive)