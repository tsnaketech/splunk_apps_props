import requests
import json
from bs4 import BeautifulSoup
import os
import hashlib
import argparse

def fetch_next_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
    return json.loads(next_data_script.string)

def generate_file(filename, content):
    content_str = json.dumps(content, indent=2)

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing_content = f.read()
        existing_hash = hashlib.md5(existing_content.encode()).hexdigest()
        new_hash = hashlib.md5(content_str.encode()).hexdigest()

        if existing_hash == new_hash:
            # print(f"File {filename} already exists and its content is identical.")
            return

    with open(filename, 'w') as f:
        f.write(content_str)
    print(f"File {filename} has been created or updated.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Retrieves data from a Splunk application and saves it to a JSON file.")
    parser.add_argument('-a', '--app_id', type=str, required=True, help="Splunk application ID")
    parser.add_argument('-d', '--directory', type=str, default='.', help="Working directory (default: current directory)")
    parser.add_argument('-o', '--output', type=str, help="Output filename (optional)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    url = f"https://splunkbase.splunk.com/app/{args.app_id}"
    
    try:
        next_data = fetch_next_data(url)

        # Extract filename from JSON
        json_filename = next_data.get('props', {}).get('pageProps', {}).get('appDetails', {}).get('release', {}).get('filename', '')

        # Split and take the first element
        filename_base = json_filename.split('_')[0] if json_filename else f"app_{args.app_id}"

        # Use user-specified filename if it exists, otherwise use default name
        output_filename = f"{args.output}.json" if args.output else f"{filename_base}.json"

        # Build the full file path
        full_path = os.path.join(args.directory, output_filename)

        # Create the working directory if it doesn't exist
        os.makedirs(args.directory, exist_ok=True)

        generate_file(full_path, next_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
