import sys
import struct

def usage():
    print("Usage: python converter.py <address>")
    print("Example: python converter.py 0x625011af")
    print("Address must be a valid 32-bit hexadecimal (start with 0x).")
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    address_str = sys.argv[1]

    # Validate and convert address
    try:
        if not address_str.startswith("0x"):
            raise ValueError("Address must start with '0x'.")

        address = int(address_str, 16)
        if not (0 <= address <= 0xFFFFFFFF):
            raise ValueError("Address out of 32-bit range.")

        little_endian = struct.pack("<I", address)
        hex_escaped = ''.join(f'\\x{byte:02x}' for byte in little_endian)

        print(f"Original address: {address_str}")
        print(f"Little Endian format: {hex_escaped}")

    except ValueError as e:
        print(f"Error: {e}")
        usage()

if __name__ == "__main__":
    main()
