import sys
import bencodepy

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

def parse_torrent(file_path):
    try:
        with open(file_path, 'rb') as file:
            bencoded_data = file.read()
        decoded_data = decode_bencode(bencoded_data)
        decoded_data = bytes_to_str(decoded_data)
        tracker_url = decoded_data.get('announce', 'Unknown')
        info_dict = decoded_data.get('info', {})
        file_length = info_dict.get('length', 'Unknown')
        
        return tracker_url, file_length
    except Exception as e:
        print(f"Error parsing torrent file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py info <torrent_file>")
        sys.exit(1)

    command = sys.argv[1]
    if command == "info":
        file_path = sys.argv[2]
        tracker_url, file_length = parse_torrent(file_path)
        print(f"Tracker URL: {tracker_url}")
        print(f"Length: {file_length}")
    else:
        print(f"Unknown command {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
