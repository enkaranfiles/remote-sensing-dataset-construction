import os
import json
import argparse

def load_json_files_from_directory(directory_path):
    combined_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                combined_data.extend(data)
    return combined_data

def save_to_json(data, output_file_path):
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def main(args):
    combined_data = load_json_files_from_directory(args.directory)
    save_to_json(combined_data, args.output_file)
    print(f"Combined data has been saved to {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine all JSON files in a directory into one JSON file.")
    parser.add_argument('directory', type=str, help="Directory containing the JSON files")
    parser.add_argument('output_file', type=str, help="Output file path for the combined JSON data")
    
    args = parser.parse_args()
    main(args)
