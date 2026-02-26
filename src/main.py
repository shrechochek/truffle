import sys
import argparse
import core

parser = argparse.ArgumentParser(description='TRUFFLE - Multi-encoding search tool')
parser.add_argument('file', help='File to search in')
parser.add_argument('search', help='Text to search for')
parser.add_argument('-i', '--iterations', type=int, default=1, 
                    help='Depth of recursive decoding (default: 1)')
parser.add_argument('-r', '--no-rot', action='store_true',
                    help='Disable ROT cipher search')

args = parser.parse_args()

if args.iterations < 1:
    print(f"{core.Colors.BRIGHT_RED}iterations must be >= 1{core.Colors.END}")
    sys.exit(1)

strings = core.get_strings(args.file)
vertical_strings = core.get_vertical_strings(strings)

print(f"{core.Colors.BRIGHT_GREEN}Started!{core.Colors.END}")

print(core.pig_art)

print(f"{core.Colors.MAGENTA}{'='*48}{core.Colors.END}")
print(f"{core.Colors.MAGENTA}{'='*14} Default Search... {'='*15}{core.Colors.END}")
print(f"{core.Colors.MAGENTA}{'='*48}{core.Colors.END}\n")
core.find_all(strings, args.search, args.iterations, not args.no_rot)

print(f"{core.Colors.MAGENTA}{'='*48}{core.Colors.END}")
print(f"{core.Colors.MAGENTA}{'='*14} Vertical Search... {'='*14}{core.Colors.END}")
print(f"{core.Colors.MAGENTA}{'='*48}{core.Colors.END}\n")
core.find_all(vertical_strings, args.search, args.iterations, not args.no_rot)

print(f"{core.Colors.BRIGHT_GREEN}Finished!{core.Colors.END}")