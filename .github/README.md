# truffle
> automatic flag search program for CTF <br>
> work like grep but support a lot of encode algorits 

[![GitHub release](https://img.shields.io/github/v/release/shrechochek/truffle?style=for-the-badge&color=ff69b4&logo=github)](https://github.com/shrechochek/truffle/releases)
![GitHub release](https://img.shields.io/github/license/shrechochek/truffle?style=for-the-badge&color=25b342&logo=github)

---

## Quick install 
```shell
git clone https://github.com/shrechochek/truffle
cd truffle
```

### Adding to paths (not required but highly recomended)
```shell
echo $SHELL # this will show you your shell
nano ~/.bashrc # or ~/.zshrc
```

then add to the end of file this 
```shell
alias truffle='python3 /full/path/to/main.py'
```

now you can run this project by typing `truffle` in your terminal

## Usage

### file search
```shell
python src/main.py FILE_NAME TEXT_TO_SEARCH [-i DEPTH] [-r] [-d] [-x KEY]
```

### recursive directory search 
```shell
python src/main.py FOLDER_NAME TEXT_TO_SEARCH [-i DEPTH] [-r] [-d] [-x KEY]
```

### Arguments
- `FILE_NAME` - file to search in
- `TEXT_TO_SEARCH` - text to search for
- `-i, --iterations DEPTH` - depth of recursive decoding (default: 1)
- `-r, --no-rot` - enable ROT cipher search
- `-d` - recursive directory search
- `-x KEY` - enable xor search with key
- `-b` - to search all `{...}` patterns

### Examples

Basic search (depth 1):
```shell
python src/main.py example.txt flag{
```

Recursive directory search (depth 3):
```shell
python src/main.py . flag{ -d -i 3
```

Recursive file search with depth 2 (finds text encoded twice):
```shell
python src/main.py file.txt flag{ -i 2
```

Recursive file search with depth 3, ROT enabled:
```shell
python src/main.py file.txt flag{ -i 3 -r
```

blind file search with depth 1:
```shell
python src/main.py file.txt -b
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
- XOR

> [!WARNING]
> Higher depths exponentially increase search time. Depth 3 without ROT = ~1,000 combinations. With ROT enabled = ~50,000+ combinations.