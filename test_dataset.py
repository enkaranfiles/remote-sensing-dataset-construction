import os
import json
from PIL import Image
from tqdm import tqdm
import argparse
import pandas as pd

def clean_json_data_enhanced(json_path, image_dir, expected_width, expected_height):
    with open(json_path, 'r') as file:
        data = json.load(file)

    initial_size = len(data)
    
    clean_data = []
    problematic_images_log = []
    id_set = set()

    for entry in tqdm(data):
        image_path = os.path.join(image_dir, entry["image"])
        
        if 'tiff' in image_path:
            image_path = image_path.replace('.tiff', '.tif')
            entry['image'] = entry['image'].replace('.tiff', '.tif')
            
        if 'JPEGImages' in image_path:
            image_path = image_path.replace('JPEGImages', '')
            entry['image'] = entry['image'].replace('JPEGImages', '')
            
        entry_valid = True

        if entry['id'] in id_set:
            entry_valid = False
        else:
            id_set.add(entry['id'])

        if not os.path.exists(image_path):
            entry_valid = False
            print(image_path)
            problematic_images_log.append((entry['id'], entry['image'], "Missing"))
        else:
            try:
                with Image.open(image_path) as img:
                    img.verify()
                    if img.size < (expected_width, expected_height):
                        entry_valid = False
                        problematic_images_log.append((entry['id'], entry['image'], "Incorrect dimensions"))
            except Exception as e:
                entry_valid = False
                problematic_images_log.append((entry['id'], entry['image'], str(e)))
        if not entry['conversations'][1]['value']:
            entry_valid = False
            problematic_images_log.append((entry['id'], entry['image'], "Empty caption"))

        if entry_valid:
            clean_data.append(entry)
    
    final_size = len(clean_data)
    return clean_data, problematic_images_log, initial_size, final_size

def save_to_json(data, output_path):
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

def save_problematic_log(problematic_log, log_path):
    with open(log_path, 'w') as log_file:
        for log_entry in problematic_log:
            log_file.write(f"ID: {log_entry[0]}, Image: {log_entry[1]}, Issue: {log_entry[2]}\n")

def generate_summary_report(problematic_log, report_path, initial_size, final_size):
    issues_count = pd.Series([entry[2] for entry in problematic_log]).value_counts()
    with open(report_path, 'w') as report_file:
        report_file.write("Summary Report:\n")
        report_file.write(f"Initial dataset size: {initial_size}\n")
        report_file.write(f"Final dataset size: {final_size}\n")
        report_file.write("Issues count:\n")
        report_file.write(issues_count.to_string())

def main(args):
    enhanced_clean_data, problematic_log, initial_size, final_size = clean_json_data_enhanced(
        args.json_file, args.image_directory, args.expected_width, args.expected_height)
    save_to_json(enhanced_clean_data, args.output_file)
    save_problematic_log(problematic_log, args.log_file)
    generate_summary_report(problematic_log, args.report_file, initial_size, final_size)
    print(f"Cleaned data has been saved to {args.output_file}")
    print(f"Problematic log has been saved to {args.log_file}")
    print(f"Summary report has been saved to {args.report_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean JSON dataset and verify image files.")
    parser.add_argument('--json_file', type=str, help="Path to the JSON file containing the dataset")
    parser.add_argument('--image_directory', type=str, help="Directory containing the image files")
    parser.add_argument('--output_file', type=str, help="Output file path for the cleaned JSON data")
    parser.add_argument('--log_file', type=str, help="Output file path for the log of problematic images")
    parser.add_argument('--report_file', type=str, help="Output file path for the summary report")
    parser.add_argument('--expected_width', type=int, help="Expected image width")
    parser.add_argument('--expected_height', type=int, help="Expected image height")
    
    args = parser.parse_args()
    main(args)
