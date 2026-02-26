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

print(core.pig_art)
core.find_all(strings, args.search, args.iterations, not args.no_rot)