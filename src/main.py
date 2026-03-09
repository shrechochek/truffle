import sys
import os
import argparse
import shutil
import core

parser = argparse.ArgumentParser(description='TRUFFLE - Multi-encoding search tool')
parser.add_argument('file', help='File to search in')
parser.add_argument('search', help='Text to search for')
parser.add_argument('-i', '--iterations', type=int, default=1, 
                    help='Depth of recursive decoding (default: 1)')
parser.add_argument('-r', '--rot', action='store_true',
                    help='Enable ROT cipher search')
parser.add_argument('-d', '--deep', action='store_true',
                    help='Recursively search all files under the provided directory')

args = parser.parse_args()

if args.iterations < 1:
    print(f"{core.Colors.BRIGHT_RED}iterations must be >= 1{core.Colors.END}")
    sys.exit(1)


def iter_target_files(path: str, deep: bool):
    if os.path.isfile(path):
        return [path]

    if not os.path.exists(path):
        print(f"{core.Colors.BRIGHT_RED}path does not exist: {path}{core.Colors.END}")
        sys.exit(1)

    if not os.path.isdir(path):
        print(f"{core.Colors.BRIGHT_RED}path is not a regular file or directory: {path}{core.Colors.END}")
        sys.exit(1)

    if not deep:
        print(f"{core.Colors.BRIGHT_RED}use -d to recursively search inside directories{core.Colors.END}")
        sys.exit(1)

    target_files = []
    for root, dirs, files in os.walk(path):
        dirs.sort()
        files.sort()
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                target_files.append(file_path)

    return target_files


def get_file_strings(file_path: str):
    try:
        return core.get_strings(file_path)
    except OSError as exc:
        print(f"{core.Colors.BRIGHT_RED}failed to read {file_path}: {exc}{core.Colors.END}")
        return None


def run_default_search(file_path: str, search_text: str, iterations: int, enable_rot: bool, deep: bool):
    strings = get_file_strings(file_path)
    if strings is None:
        return 0

    source_label = file_path if deep else None
    return core.find_all(strings, search_text, iterations, enable_rot, source_label)


def run_vertical_search(file_path: str, search_text: str, iterations: int, enable_rot: bool, deep: bool):
    strings = get_file_strings(file_path)
    if strings is None:
        return 0

    vertical_strings = core.get_vertical_strings(strings)
    source_label = file_path if deep else None
    return core.find_all(vertical_strings, search_text, iterations, enable_rot, source_label)

target_files = iter_target_files(args.file, args.deep)

print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_GREEN}Started!{core.Colors.END}")

columns = shutil.get_terminal_size(fallback=(80, 24)).columns

if columns >= 84:
    print(core.main_text_and_pig_art)
elif columns >= 53:
    print(core.main_text)
elif columns >= 32:
    print(core.pig_art)

search_text = " Default Search... "
spaces_len = (columns-len(search_text))//2
print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'='*columns}{core.Colors.END}")
print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'='*spaces_len} Default Search... {'='*(spaces_len+(columns-len(search_text))%2)}{core.Colors.END}")
print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'='*columns}{core.Colors.END}\n")
for file_path in target_files:
    run_default_search(file_path, args.search, args.iterations, args.rot, args.deep)


vertical_search_text = " Vertical Search... "
spaces_len = (columns-len(vertical_search_text))//2
print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'='*columns}{core.Colors.END}")
print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'='*spaces_len}{vertical_search_text}{'='*(spaces_len+(columns-len(vertical_search_text))%2)}{core.Colors.END}")
print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'='*columns}{core.Colors.END}\n")
for file_path in target_files:
    run_vertical_search(file_path, args.search, args.iterations, args.rot, args.deep)

print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_GREEN}Finished!{core.Colors.END}")