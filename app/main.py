import sys
import bencodepy
import hashlib
import json

def decode_bencode(bencoded_value):
    return bencodepy.decode(bencoded_value)

def bytes_to_str(data):
    if isinstance(data, bytes):
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return data  # Return raw bytes if decoding fails
    elif isinstance(data, list):
        return [bytes_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {bytes_to_str(key): bytes_to_str(value) for key, value in data.items()}
    else:
        return data

def parse_torrent(file_path):
    try:
        with open(file_path, 'rb') as file:
            bencoded_data = file.read()
        decoded_data = decode_bencode(bencoded_data)
        tracker_url = decoded_data.get(b'announce', b'Unknown').decode('utf-8')
        info_dict = decoded_data.get(b'info', {})
        file_length = info_dict.get(b'length', 'Unknown')

        # Bencode the info dictionary and calculate the SHA-1 hash
        bencoded_info_dict = bencodepy.encode(info_dict)
        info_hash = hashlib.sha1(bencoded_info_dict).hexdigest()
        #Extract length and piece
        piece_length=info_dict.get(b'piece length', 'Unknown')
        pieces = info_dict.get(b'pieces', b'')
        piece_hashes = [pieces[i:i+20].hex() for i in range(0, len(pieces), 20)]
        return tracker_url, file_length, info_hash, piece_length, piece_hashes
    except Exception as e:
        print(f"Error parsing torrent file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:  # Check for at least 2 arguments
        print("Usage: python script.py <command> [args]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "decode":  # Handling the decode command
        if len(sys.argv) != 3:  # Check for the correct number of arguments
            print("Usage: python script.py decode <bencoded_string>")
            sys.exit(1)
        bencoded_value = sys.argv[2].encode()
        try:
            decoded_value = decode_bencode(bencoded_value)
            converted_value = bytes_to_str(decoded_value)
            print(json.dumps(converted_value))
        except Exception as e:
            print(f"Error decoding bencoded value: {e}")
            sys.exit(1)
    elif command == "info":  # Handling the info command
        if len(sys.argv) != 3:  # Check for the correct number of arguments
            print("Usage: python script.py info <torrent_file>")
            sys.exit(1)
        file_path = sys.argv[2]
        tracker_url, file_length, info_hash,piece_length, piece_hashes = parse_torrent(file_path)
        print(f"Tracker URL: {tracker_url}")
        print(f"Length: {file_length}")
        print(f"Info Hash: {info_hash}")
        print(f"Piece Length: {piece_length}")
        print(f"Piece Hashes:{piece_hashes}")
        for piece_hash in piece_hashes:
            print(piece_hash)
    else:
        print(f"Unknown command {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
