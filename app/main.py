import json
import sys
import bencodepy

def decode_bencode(bencoded_value):
    return bencodepy.decode(bencoded_value)

def bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode()
    elif isinstance(data, list):
        return [bytes_to_str(item) for item in data]
    elif isinstance(data, dict):
         # Ensure both keys and values are converted to strings
        return {bytes_to_str(key): bytes_to_str(value) for key, value in data.items()}
    else:
        return data  # Return the data as is if it's not bytes, list, or dict
def main():
    command = sys.argv[1]
    if command == "decode":
        bencoded_value = sys.argv[2].encode()
        decoded_value = decode_bencode(bencoded_value)
        print(json.dumps(decoded_value, default=bytes_to_str))
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
