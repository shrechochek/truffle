# truffle
> automatic flag search program for CTF

---

## Quick install 
```shell
git clone https://github.com/shrechochek/truffle
cd truffle
```

## Usage
```shell
python src/main.py FILE_NAME TEXT_TO_SEARCH [-i DEPTH] [-r]
```

### Arguments
- `FILE_NAME` - file to search in
- `TEXT_TO_SEARCH` - text to search for
- `-i, --iterations DEPTH` - depth of recursive decoding (default: 1)
- `-r, --no-rot` - disable ROT cipher search

### Examples

Basic search (depth 1):
```shell
python src/main.py example.txt flag{

Found results for base64_search
index: 16
fdsfsadfdsffflag{hello_test}fdfdasfdsfaffdasffieu
```

Recursive search with depth 2 (finds text encoded twice):
```shell
python src/main.py file.txt secret -i 2

Searching with depth 2... This may take a while.

Found results for chain: base58 → base64
Original text: HbLESKAYodh
secret
```

Recursive search with depth 3, ROT disabled:
```shell
python src/main.py file.txt flag -i 3 -r

Searching with depth 3... This may take a while.

Found results for chain: base64 → base64_reverse → no_decode
Original text: PT13TXlFRGR6Vkdk
```

## Supported Encodings
- Base64, Base58, Base32, Base45, Base62, Base85, Base92
- Hexadecimal
- Binary (with/without spaces)
- ROT (all 25 variants)
- Morse code
- Atbash cipher
- URL encoding
- Reverse (for all encodings)

> [!WARNING]
> Higher depths exponentially increase search time. Depth 3 without ROT = ~1,000 combinations. With ROT enabled = ~50,000+ combinations.