import sys
import os
import argparse
import shutil
import core

parser = argparse.ArgumentParser(description='TRUFFLE - Multi-encoding search tool')
parser.add_argument('file', help='File to search in')
parser.add_argument('search', nargs='?', help='Text to search for')
parser.add_argument('-i', '--iterations', type=int, default=1, 
                    help='Depth of recursive decoding (default: 1)')
parser.add_argument('-r', '--rot', action='store_true',
                    help='Enable ROT cipher search')
parser.add_argument('-d', '--deep', action='store_true',
                    help='Recursively search all files under the provided directory')
parser.add_argument('-x', '--xor', dest='xor_key',
                    help='Enable XOR search using the provided key (string or 0xNN)')
parser.add_argument('-b', '--blind', action='store_true',
                    help='Blindly search for constructs like {some text}')

args = parser.parse_args()

if args.iterations < 1:
    print(f"{core.Colors.BRIGHT_RED}iterations must be >= 1{core.Colors.END}")
    sys.exit(1)

if args.xor_key == "":
    print(f"{core.Colors.BRIGHT_RED}xor key must not be empty{core.Colors.END}")
    sys.exit(1)

if args.search is None and not args.blind:
    parser.error('search is required unless -b/--blind is used')


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


def build_progress_label(stage: str, file_index: int, total_files: int, deep: bool):
    if deep:
        return f"{stage} file {file_index}/{total_files}"

    return stage


def print_stage_banner(title: str, columns: int):
    core.clear_status()
    banner_text = f" {title} "
    spaces_len = (columns - len(banner_text)) // 2
    print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'=' * columns}{core.Colors.END}")
    print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'=' * spaces_len}{banner_text}{'=' * (spaces_len + (columns - len(banner_text)) % 2)}{core.Colors.END}")
    print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_MAGENTA}{'=' * columns}{core.Colors.END}\n")


def run_default_search(file_path: str, search_text: str | None, iterations: int, enable_rot: bool, deep: bool, xor_key: str | None, progress_label: str, blind_mode: bool):
    strings = get_file_strings(file_path)
    if strings is None:
        return 0

    source_label = file_path if deep else None
    return core.find_all(strings, search_text, iterations, enable_rot, source_label, xor_key, progress_label, blind_mode)


def run_vertical_search(file_path: str, search_text: str | None, iterations: int, enable_rot: bool, deep: bool, xor_key: str | None, progress_label: str, blind_mode: bool):
    strings = get_file_strings(file_path)
    if strings is None:
        return 0

    vertical_strings = core.get_vertical_strings(strings)
    source_label = file_path if deep else None
    return core.find_all(vertical_strings, search_text, iterations, enable_rot, source_label, xor_key, progress_label, blind_mode)

target_files = iter_target_files(args.file, args.deep)

print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_GREEN}Started!{core.Colors.END}")

columns = shutil.get_terminal_size(fallback=(80, 24)).columns

if columns >= 84:
    print(core.pig_art_and_main_text)
elif columns >= 53:
    print(core.main_text)
elif columns >= 32:
    print(core.pig_art)

print_stage_banner("Default Search...", columns)
for file_index, file_path in enumerate(target_files, start=1):
    run_default_search(
        file_path,
        args.search,
        args.iterations,
        args.rot,
        args.deep,
        args.xor_key,
        build_progress_label("Default Search:", file_index, len(target_files), args.deep),
        args.blind,
    )
print_stage_banner("Vertical Search...", columns)
for file_index, file_path in enumerate(target_files, start=1):
    run_vertical_search(
        file_path,
        args.search,
        args.iterations,
        args.rot,
        args.deep,
        args.xor_key,
        build_progress_label("Vertical Search:", file_index, len(target_files), args.deep),
        args.blind,
    )

core.clear_status()

print(f"{core.Colors.BOLD}{core.Colors.BRIGHT_GREEN}Finished!{core.Colors.END}")