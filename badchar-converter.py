#!/usr/bin/env python3

import sys

def usage():
    print("Usage: python3 badchar-converter.py <bad chars>")
    print("Example: python3 badchar-converter.py 23 24 3c 3d 83 81 ba bb")
    sys.exit(1)

def is_valid_hex(h):
    return len(h) == 2 and all(c in "0123456789abcdefABCDEF" for c in h)

def main():
    if len(sys.argv) < 2:
        usage()

    badchars = sys.argv[1:]
    escaped = ["\\x00"]  # Start with null byte by default

    for hex_byte in badchars:
        hex_byte = hex_byte.lower()
        if not is_valid_hex(hex_byte):
            print(f"Invalid hex byte: {hex_byte}")
            usage()
        escaped.append(f"\\x{hex_byte}")

    output = ''.join(escaped)
    print(f"{output}")

if __name__ == "__main__":
    main()
