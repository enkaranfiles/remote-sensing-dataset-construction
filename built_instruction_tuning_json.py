import json
import os
import argparse
from collections import defaultdict
from tqdm import tqdm


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def consolidate_conversations(data):
    consolidated_data = defaultdict(lambda: {"id": "", "image": "", "conversations": []})
    
    for entry in data:
        image = entry['image']
        
        # Use image as the key to consolidate entries
        if not consolidated_data[image]["image"]:
            consolidated_data[image]["image"] = image
        
        consolidated_data[image]["conversations"].extend(entry["conversations"])
    
    return list(consolidated_data.values())

def consolidate_all_files(directory):
    all_consolidated_data = []
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    for filename in tqdm(json_files, desc="Processing JSON files"):
        file_path = os.path.join(directory, filename)
        data = load_json_data(file_path)
        consolidated_data = consolidate_conversations(data)
        all_consolidated_data.extend(consolidated_data)
    
    # Assign consecutive IDs to the combined data
    for idx, entry in enumerate(all_consolidated_data):
        entry["id"] = str(idx)
    
    return all_consolidated_data

def save_to_json(data, output_file_path):
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def main(args):
    consolidated_data = consolidate_all_files(args.directory)
    save_to_json(consolidated_data, args.output_file)
    print(f"Consolidated data from all files has been saved to {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consolidate conversations from multiple JSON files in a directory.")
    parser.add_argument('--directory', type=str, default='dataset/json_files', help="Directory containing the JSON files")
    parser.add_argument('--output_file', type=str, default='instruction-tuning-dataset/instruction_tuning_dataset.json', help="Output file path for the consolidated JSON data")
    
    args = parser.parse_args()
    main(args)
