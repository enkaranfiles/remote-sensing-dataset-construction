import json
import os
import argparse

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def convert_floodnet_format(floodnet_data, img_root):
    new_format_data = []
    for key, value in floodnet_data.items():
        new_entry = {
            "id": key,
            "image": os.path.join(img_root, value["Image_ID"]),
            "conversations": [
                {
                    "from": "human",
                    "value": "<image>\n" + value["Question"]
                },
                {
                    "from": "gpt",
                    "value": value["Ground_Truth"]
                }
            ]
        }
        new_format_data.append(new_entry)
    return new_format_data

def save_to_json(data, output_file_path):
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def main(args):
    floodnet_data = load_json_data(args.floodnet_file)
    converted_data = convert_floodnet_format(floodnet_data, args.img_root)
    save_to_json(converted_data, args.output_file)
    print(f"Converted data has been saved to {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert FloodNet dataset to instruction tuning dataset format.")
    parser.add_argument('floodnet_file', type=str, help="Path to the JSON file containing FloodNet questions data")
    parser.add_argument('img_root', type=str, help="Root directory path for FloodNet images")
    parser.add_argument('output_file', type=str, help="Output file path for the converted JSON data")
    
    args = parser.parse_args()
    main(args)
