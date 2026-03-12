import os
import sys
import re
import shutil
from functools import lru_cache
from itertools import zip_longest

import decoders
import encoders
import searchers


# ---------- Art & banners
pig_art = r"""
          ⣀⣤⣤⣶⣶⣶⣶⣦⣤⣄⣀           
 ⢀⡶⢻⡦⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣴⣾⡿ ⣠ 
 ⠠⣬⣷⣾⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣌⣋⣉⣄⠘⠋  
   ⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡄    
   ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣷⣶⡄ 
   ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇ 
   ⠸⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠻⠿⣿⣿⡿⠛⠛⠛⠋⠉⠉   
    ⢻⣿⣿  ⢸⣿⡇     ⢻⣿⠃⠸⣿⡇      
    ⠈⠿⠇   ⠻⠇     ⠈⠿  ⠻⠿
"""

main_text = r"""
  _______ _____  _    _ ______ ______ _      ______ 
 |__   __|  __ \| |  | |  ____|  ____| |    |  ____|
    | |  | |__) | |  | | |__  | |__  | |    | |__   
    | |  |  _  /| |  | |  __| |  __| | |    |  __|   
    | |  | | \ \| |__| | |    | |    | |____| |____  
    |_|  |_|  \_\\____/|_|    |_|    |______|______|   
"""

# Combined banner for large terminals
main_text_and_pig_art = main_text + "\n" + pig_art


# ---------- Terminal & patterns
TERMINAL_SIZE = shutil.get_terminal_size(fallback=(80, 24))
STATUS_COLS = TERMINAL_SIZE.columns
STATUS_ROW = TERMINAL_SIZE.lines
STATUS_ENABLED = sys.stdout.isatty()
ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
BLIND_FLAG_PATTERN = re.compile(r"\{[^{}\r\n]+\}")

PRINTABLE_ASCII_PATTERN = re.compile(rb"[\x20-\x7e]{4,}")
POTENTIAL_ENCODED_PATTERN = re.compile(r"[A-Za-z0-9+/=\-_.~%:$#@!*]+")

MORSE_CHARS = frozenset(".-")
BINARY_CHARS = frozenset("01 ")
HEX_CHARS = frozenset("0123456789ABCDEFabcdef")
BASE64_CHARS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
)
BASE32_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=")
BASE45_CHARS = frozenset("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:")
BASE58_FORBIDDEN = frozenset("0OIl")
BASE85_SPECIAL_CHARS = frozenset(".-:+=^!/*?&<>()[]{}@%$#")
BASE92_SPECIAL_CHARS = frozenset("!#$%&'()*+,-./:;<=>?@[]^_`{|}~")


# Base decoders list (name, func, param, is_reverse)
BASE_DECODERS = [
    ("no_decode", decoders.no_decode, None, False),
    ("base64", decoders.decode_base64, None, False),
    ("base64_reverse", decoders.decode_base64, None, True),
    ("base58", decoders.decode_base58, None, False),
    ("base58_reverse", decoders.decode_base58, None, True),
    ("base32", decoders.decode_base32, None, False),
    ("base32_reverse", decoders.decode_base32, None, True),
    ("base45", decoders.decode_base45, None, False),
    ("base45_reverse", decoders.decode_base45, None, True),
    ("base62", decoders.decode_base62, None, False),
    ("base62_reverse", decoders.decode_base62, None, True),
    ("base85", decoders.decode_base85, None, False),
    ("base85_reverse", decoders.decode_base85, None, True),
    ("base92", decoders.decode_base92, None, False),
    ("base92_reverse", decoders.decode_base92, None, True),
    ("hex", decoders.decode_hex, None, False),
    ("hex_reverse", decoders.decode_hex, None, True),
    ("binary", decoders.decode_binary, None, False),
    ("binary_reverse", decoders.decode_binary, None, True),
    ("morse", decoders.decode_morse, None, False),
    ("morse_reverse", decoders.decode_morse, None, True),
    ("atbash", decoders.decode_atbash, None, False),
    ("atbash_reverse", decoders.decode_atbash, None, True),
    ("url", decoders.decode_url, None, False),
    ("url_reverse", decoders.decode_url, None, True),
]


class Colors:
    END = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    STRIKETHROUGH = "\033[9m"
    REVERSE = "\033[7m"
    INVISIBLE = "\033[8m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


# ----------------- Performance cache used by optimized decoders -----------------
# Keep a simple in-memory cache for full decode results to avoid repeated heavy
# decoding operations (an important optimization for large inputs)
_DECODE_CACHE: dict = {}


def _call_decoder_cached(decoder_func, candidate: str, param=None):
    key = (decoder_func.__name__, candidate, param)
    if key in _DECODE_CACHE:
        return _DECODE_CACHE[key]
    try:
        if param is not None:
            res = decoder_func(candidate, param)
        else:
            res = decoder_func(candidate)
    except Exception:
        res = None
    _DECODE_CACHE[key] = res
    return res


# ----------------- Utility functions -----------------
def _truncate_ansi_text(text: str, max_visible_chars: int) -> str:
    visible_chars = 0
    position = 0
    result = []

    while position < len(text) and visible_chars < max_visible_chars:
        escape_match = ANSI_ESCAPE_PATTERN.match(text, position)
        if escape_match:
            result.append(escape_match.group(0))
            position = escape_match.end()
            continue

        result.append(text[position])
        visible_chars += 1
        position += 1

    truncated = "".join(result)
    if "\033[" in truncated and not truncated.endswith(Colors.END):
        truncated += Colors.END

    return truncated


STATUS_VISIBLE = False


def status(msg: str):
    if not STATUS_ENABLED:
        return
    global STATUS_VISIBLE
    sys.stdout.write("\r\033[2K")
    sys.stdout.write(_truncate_ansi_text(msg, max(1, STATUS_COLS - 1)))
    sys.stdout.flush()
    STATUS_VISIBLE = True


def clear_status():
    if not STATUS_ENABLED:
        return
    global STATUS_VISIBLE
    if not STATUS_VISIBLE:
        return
    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()
    STATUS_VISIBLE = False


def _format_progress(label: str, current: int, total: int, extra: str = "") -> str:
    total = max(total, 1)
    current = min(max(current, 0), total)
    percent = current / total
    bar_width = max(10, min(30, STATUS_COLS // 3))
    filled = int(bar_width * percent)
    bar = (
        Colors.BG_GREEN
        + " " * filled
        + Colors.END
        + Colors.BG_RED
        + " " * (bar_width - filled)
        + Colors.END
    )
    message = f"{Colors.CYAN}{label}{Colors.END} {bar} {Colors.GREEN}{current}{Colors.END}/{total} {percent * 100:5.1f}%"
    if extra:
        message = f"{message} {extra}"
    return message


# ----------------- String extraction -----------------
def get_strings(file_path: str, min_len: int = 4) -> list[str]:
    # Preserve unicode printable extraction to support non-ASCII files (e.g. Cyrillic)
    with open(file_path, "rb") as f:
        content = f.read()

    decoded_content = content.decode("utf-8", errors="ignore")
    result = []
    current_chars = []

    for ch in decoded_content:
        if ch.isprintable():
            current_chars.append(ch)
            continue

        if len(current_chars) >= min_len:
            result.append("".join(current_chars))
        current_chars = []

    if len(current_chars) >= min_len:
        result.append("".join(current_chars))

    return result


def get_vertical_strings(text: list[str]) -> list[str]:
    if not text:
        return []
    return ["".join(column) for column in zip_longest(*text, fillvalue="")]


def find_all_indices(text: str, substring: str) -> list[int]:
    indices = []
    start = 0
    while True:
        idx = text.find(substring, start)
        if idx == -1:
            break
        indices.append(idx)
        start = idx + 1
    return indices


# ----------------- Searcher / decoder orchestration -----------------
searcher_functions = [
    searchers.default_search,
    searchers.default_reverse_search,
    searchers.base64_search,
    searchers.base64_reverse_search,
    searchers.base58_search,
    searchers.base58_reverse_search,
    searchers.base32_search,
    searchers.base32_reverse_search,
    searchers.base45_search,
    searchers.base45_reverse_search,
    searchers.base62_search,
    searchers.base62_reverse_search,
    searchers.base85_search,
    searchers.base85_reverse_search,
    searchers.base92_search,
    searchers.base92_reverse_search,
    searchers.hex_search,
    searchers.hex_reverse_search,
    searchers.rot_search,
    searchers.rot_reverse_search,
    searchers.binary_search,
    searchers.binary_reverse_search,
    searchers.morse_search,
    searchers.morse_reverse_search,
    searchers.atbash_search,
    searchers.atbash_reverse_search,
    searchers.url_search,
    searchers.url_reverse_search,
    # xor searchers may be appended dynamically when xor_key provided
]

decoder_functions = [
    decoders.no_decode,
    decoders.decode_base64,
    decoders.decode_base58,
    decoders.decode_base32,
    decoders.decode_base45,
    decoders.decode_base62,
    decoders.decode_base85,
    decoders.decode_base92,
    decoders.decode_hex,
    decoders.decode_rot,
    decoders.decode_binary,
    decoders.decode_morse,
    decoders.decode_atbash,
    decoders.decode_url,
]


def find_all(
    strings: list[str],
    search_text: str | None,
    max_depth: int = 1,
    enable_rot: bool = False,
    source_label: str | None = None,
    xor_key: str | None = None,
    progress_label: str | None = None,
    blind_mode: bool = False,
) -> int:
    """Top-level entry. Keeps optimized behavior while supporting extra
    parameters (xor_key, progress_label, blind_mode)."""
    if not strings:
        return 0

    plain_strings = "".join(strings)
    return _find_recursive(
        plain_strings,
        strings,
        search_text,
        max_depth,
        enable_rot,
        source_label,
        xor_key,
        progress_label,
        blind_mode,
    )


def _find_recursive(
    plain_strings: str,
    strings: list[str],
    search_text: str | None,
    max_depth: int,
    enable_rot: bool,
    source_label: str | None = None,
    xor_key: str | None = None,
    progress_label: str | None = None,
    blind_mode: bool = False,
) -> int:
    # Warn for expensive searches
    if max_depth > 5 or (max_depth > 2 and enable_rot):
        clear_status()
        print(
            f"{Colors.BRIGHT_CYAN}Searching with depth {max_depth}... This may take a while.{Colors.END}\n"
        )

    base_decoders = _get_base_decoders(enable_rot, xor_key)
    potential_encoded = _collect_potential_encoded(strings, plain_strings)
    found_results = set()
    total_candidates = len(potential_encoded)

    # progress bar via status if requested
    if progress_label and total_candidates > 0:
        status(_format_progress(progress_label, 0, total_candidates))

    update_interval = max(1, total_candidates // 100) if total_candidates > 0 else 1

    for index, encoded_text in enumerate(potential_encoded, start=1):
        _walk_decoder_chains(
            encoded_text,
            encoded_text,
            search_text,
            base_decoders,
            max_depth,
            [],
            found_results,
            source_label,
            blind_mode,
        )

        if progress_label and (
            index == 1 or index == total_candidates or index % update_interval == 0
        ):
            extra = ""
            if source_label:
                extra = f"{os.path.basename(source_label)} {extra}"
            status(_format_progress(progress_label, index, total_candidates, extra))

    if progress_label and total_candidates == 0:
        extra = (
            f"{os.path.basename(source_label)} no-candidates"
            if source_label
            else "no-candidates"
        )
        status(_format_progress(progress_label, 1, 1, extra))

    return len(found_results)


def _get_base_decoders(enable_rot: bool, xor_key: str | None = None):
    base_decoders = list(BASE_DECODERS)

    if enable_rot:
        for offset in range(1, 26):
            base_decoders.append((f"rot{offset}", decoders.decode_rot, offset, False))
            base_decoders.append(
                (f"rot{offset}_reverse", decoders.decode_rot, offset, True)
            )

    if xor_key is not None:
        # include xor decoder with provided key
        base_decoders.append((f"xor({xor_key})", decoders.decode_xor, xor_key, False))
        base_decoders.append(
            (f"xor({xor_key})_reverse", decoders.decode_xor, xor_key, True)
        )

    return base_decoders


def _collect_potential_encoded(strings: list[str], plain_strings: str) -> set[str]:
    potential_encoded = set()
    for s in strings:
        stripped = s.strip()
        if len(stripped) >= 4:
            potential_encoded.add(stripped)

        for match in POTENTIAL_ENCODED_PATTERN.findall(s):
            sm = match.strip()
            if len(sm) >= 4:
                potential_encoded.add(sm)

    # also chunk the whole plain text to find longer candidates
    for i in range(0, len(plain_strings), 30):
        chunk = plain_strings[i : min(i + 150, len(plain_strings))].strip()
        if len(chunk) >= 4:
            potential_encoded.add(chunk)

    return potential_encoded


def _walk_decoder_chains(
    original_text: str,
    current_text: str,
    search_text: str | None,
    base_decoders,
    depth_left: int,
    chain_names: list[str],
    found_results: set,
    source_label: str | None = None,
    blind_mode: bool = False,
):
    # depth-left 0: check for match and register
    if depth_left == 0:
        match_text = _find_match_text(current_text, search_text, blind_mode)
        if match_text is not None:
            chain_str = " → ".join(chain_names)
            key = (chain_str, current_text[:100])
            if key not in found_results:
                found_results.add(key)
                _print_result(
                    {
                        "index": original_text.find(current_text),
                        "chain_str": chain_str,
                        "decoded": current_text,
                        "match_text": match_text,
                    },
                    source_label,
                )
        return

    for name, decoder_func, param, is_reverse in base_decoders:
        # skip unlikely encodings and redundant chains
        if _should_skip_decoder(chain_names, name, param, is_reverse):
            continue

        if not _can_be_encoding(current_text, name):
            continue

        candidate = current_text[::-1] if is_reverse else current_text

        try:
            # partial scan helper: if available, use it for long searches to avoid full decode
            partial = getattr(decoders, "_partial_scan", None)
            use_partial = partial is not None and (
                search_text is not None and len(search_text) >= 8
            )

            partial_result = None
            if partial is not None and use_partial:
                try:
                    if param is not None:
                        partial_result = partial(
                            decoder_func, candidate, search_text, param
                        )
                    else:
                        partial_result = partial(decoder_func, candidate, search_text)
                except Exception:
                    partial_result = None

            if partial_result:
                narrowed = partial_result[0]
                chain_names.append(name)
                _walk_decoder_chains(
                    original_text,
                    narrowed,
                    search_text,
                    base_decoders,
                    depth_left - 1,
                    chain_names,
                    found_results,
                    source_label,
                    blind_mode,
                )
                chain_names.pop()
                if globals().get("_STOP_ON_FIRST") and globals().get("_FOUND_ANY"):
                    return
                continue

            # try cached decode when possible
            if search_text is None:
                dec_result = _call_decoder_cached(decoder_func, candidate, param)
            else:
                if param is not None:
                    try:
                        dec_result = decoder_func(
                            candidate, param, search_text=search_text
                        )
                    except TypeError:
                        dec_result = decoder_func(candidate, param)
                else:
                    try:
                        dec_result = decoder_func(candidate, search_text=search_text)
                    except TypeError:
                        dec_result = decoder_func(candidate)
        except Exception:
            continue

        if not dec_result:
            continue

        # normalize result
        if isinstance(dec_result, (list, tuple)):
            decoded_text = dec_result[0]
        else:
            decoded_text = dec_result

        # check for match_text (including blind mode) before recursing
        match_text = _find_match_text(decoded_text, search_text, blind_mode)
        if match_text is not None:
            chain_names.append(name)
            chain_str = " → ".join(chain_names)
            key = (chain_str, decoded_text[:100])
            if key not in found_results:
                found_results.add(key)
                _print_result(
                    {
                        "index": original_text.find(decoded_text),
                        "chain_str": chain_str,
                        "decoded": decoded_text,
                        "match_text": match_text,
                    },
                    source_label,
                )
            chain_names.pop()
            continue

        # otherwise recurse deeper
        chain_names.append(name)
        _walk_decoder_chains(
            original_text,
            decoded_text,
            search_text,
            base_decoders,
            depth_left - 1,
            chain_names,
            found_results,
            source_label,
            blind_mode,
        )
        chain_names.pop()


def _find_match_text(
    text: str, search_text: str | None, blind_mode: bool
) -> str | None:
    if search_text and search_text in text:
        return search_text
    if blind_mode:
        m = BLIND_FLAG_PATTERN.search(text)
        if m:
            return m.group(0)
    return None


def _get_decoder_family(name: str) -> str:
    if name.startswith("no_decode"):
        return "identity"
    if name.startswith("rot"):
        return "rot"
    if name.startswith("xor("):
        return "xor"
    if name.startswith("atbash"):
        return "atbash"
    if name.endswith("_reverse"):
        return name[:-8]
    return name


@lru_cache(maxsize=64)
def _is_single_byte_xor_key(key: str | None) -> bool:
    if key is None:
        return False
    if key.lower().startswith("0x"):
        try:
            return 0 <= int(key, 16) <= 0xFF
        except ValueError:
            return False
    return len(key.encode("utf-8")) == 1


def _should_skip_decoder(
    chain_names: list[str], name: str, param, is_reverse: bool
) -> bool:
    if not chain_names:
        return False
    prev = chain_names[-1]
    prev_family = _get_decoder_family(prev)
    cur_family = _get_decoder_family(name)
    if prev_family == "rot" and cur_family == "rot":
        return True
    if prev_family == "atbash" and cur_family == "atbash":
        return True
    if prev_family == "identity" and cur_family == "identity":
        return True
    if prev_family == "xor" and cur_family == "xor":
        prev_is_rev = prev.endswith("_reverse")
        prev_base = prev[:-8] if prev_is_rev else prev
        prev_key = prev_base[4:-1] if prev_base.startswith("xor(") else None
        if prev_key == param and not prev_is_rev and not is_reverse:
            return True
        if prev_key == param and _is_single_byte_xor_key(param):
            return True
    return False


@lru_cache(maxsize=16384)
def _can_be_encoding(text: str, encoding_name: str) -> bool:
    if not text:
        return False
    en = encoding_name.lower()
    if "url" in en:
        return "%" in text and any(c in HEX_CHARS for c in text)
    if "morse" in en:
        return any(c in MORSE_CHARS for c in text) and not any(
            c.isalnum() for c in text.replace(" ", "")
        )
    if "binary" in en:
        return len(text) >= 8 and all(c in BINARY_CHARS for c in text)
    if "hex" in en:
        return len(text) >= 2 and all(c in HEX_CHARS for c in text)
    if "base64" in en:
        return len(text) >= 4 and all(c in BASE64_CHARS for c in text)
    if "base58" in en:
        return not any(c in BASE58_FORBIDDEN for c in text) and text.isalnum()
    if "base32" in en:
        return len(text) >= 4 and all(c in BASE32_CHARS for c in text.upper())
    if "base45" in en:
        return all(c in BASE45_CHARS for c in text.upper())
    if "base62" in en:
        return text.isalnum() and len(text) >= 4
    if "base85" in en:
        return len(text) >= 5 and any(c in BASE85_SPECIAL_CHARS for c in text)
    if "base92" in en:
        return len(text) >= 4 and any(c in BASE92_SPECIAL_CHARS for c in text)
    if "rot" in en:
        return any(c.isalpha() for c in text)
    if "atbash" in en:
        return any(c.isalpha() for c in text)
    if "no_decode" in en:
        return True
    return True


def _print_result(result, source_label: str | None = None):
    # clear terminal status and print nicely
    clear_status()
    if source_label:
        print(f"{Colors.BRIGHT_BLUE}File: {source_label}{Colors.END}")
    print(
        f"Found results for chain: {Colors.BRIGHT_YELLOW}{result['chain_str']}{Colors.END}"
    )
    if "index" in result:
        print(f"{Colors.BRIGHT_GREEN}Index: {result['index']}{Colors.END}")

    decoded = result.get("decoded", "")
    match_text = result.get("match_text")
    if match_text:
        pos = decoded.find(match_text)
        if pos == -1:
            print(decoded[:80])
            print()
        else:
            after_start = pos + len(match_text)
            brace_pos = decoded.find("}", after_start)
            if brace_pos != -1 and brace_pos - after_start <= 65:
                after_end = brace_pos + 1
            else:
                after_end = min(len(decoded), after_start + 65)
            context_start = max(0, pos - 50)
            before = decoded[context_start:pos]
            after = decoded[after_start:after_end]
            print(f"{before}{Colors.BOLD}{Colors.RED}{match_text}{Colors.END}{after}")
            print()
    else:
        print(decoded[:200])
        print()

    try:
        globals()["_FOUND_ANY"] = True
    except Exception:
        pass
