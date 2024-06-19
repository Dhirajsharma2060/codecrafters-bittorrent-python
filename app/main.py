import json
import sys

def decode_bencode(data):
    if data.startswith(b'i'):
        return decode_integer(data)
    elif data.startswith(b'l'):
        return decode_list(data)
    elif data.startswith(b'd'):
        return decode_dict(data)
    elif data[0:1].isdigit():
        return decode_string(data)
    else:
        raise ValueError("Invalid bencoded data")

def decode_integer(data):
    end = data.index(b'e')
    number = int(data[1:end])
    rest = data[end+1:]
    return number, rest

def decode_string(data):
    colon = data.index(b':')
    length = int(data[:colon])
    start = colon + 1
    end = start + length
    string = data[start:end]
    rest = data[end:]
    return string, rest

def decode_list(data):
    items = []
    data = data[1:]  # remove the leading 'l'
    while not data.startswith(b'e'):
        item, data = decode_bencode(data)
        items.append(item)
    rest = data[1:]  # remove the trailing 'e'
    return items, rest

def decode_dict(data):
    items = {}
    data = data[1:]  # remove the leading 'd'
    while not data.startswith(b'e'):
        key, data = decode_string(data)
        value, data = decode_bencode(data)
        items[key.decode('utf-8')] = value
    rest = data[1:]  # remove the trailing 'e'
    return items, rest

def bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    elif isinstance(data, list):
        return [bytes_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: bytes_to_str(value) for key, value in data.items()}
    else:
        return data

def main():
    command = sys.argv[1]
    if command == "decode":
        bencoded_value = sys.argv[2].encode('utf-8')
        decoded_value, _ = decode_bencode(bencoded_value)
        converted_value = bytes_to_str(decoded_value)
        print(json.dumps(converted_value))
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
