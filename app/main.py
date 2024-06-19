import json
import sys
import bencodepy

# Initialize the bencodepy Bencode class
bc = bencodepy.Bencode(encoding="utf-8")

def decode_bencode(bencoded_value):
    return bencodepy.decode(bencoded_value)

def bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    elif isinstance(data, list):
        return [bytes_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {bytes_to_str(key): bytes_to_str(value) for key, value in data.items()}
    else:
        return data

def main():
    command = sys.argv[1]
    if command == "decode":
        bencoded_value = sys.argv[2].encode()
        decoded_value = decode_bencode(bencoded_value)
        converted_value = bytes_to_str(decoded_value)
        print(json.dumps(converted_value))
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
