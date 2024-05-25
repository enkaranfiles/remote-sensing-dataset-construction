import pandas as pd
import json
import os
import random
import argparse

def load_dataframe(file_path):
    return pd.read_csv(file_path)

def filter_dataframe(df, column, value):
    return df[df[column] == value]

def dataframe_to_format(df, questions, img_root):
    new_format_data = []
    for _, row in df.iterrows():
        image_path = os.path.join(img_root, row['filename'])
        
        # Check if the image file exists
        if os.path.exists(image_path):
            question = random.choice(questions)
            new_entry = {
                "id": str(row['id']),
                "image": image_path,
                "conversations": [
                    {
                        "from": "human",
                        "value": f"<image>\n{question}"
                    },
                    {
                        "from": "gpt",
                        "value": row['caption']
                    }
                ]
            }
            new_format_data.append(new_entry)
        else:
            print(f"Image file does not exist: {image_path}")  # Optional: for logging missing files
    return new_format_data

def save_to_json(data, output_file_path):
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def main(args):
    df = load_dataframe(args.input_file)
    df = filter_dataframe(df, 'lang', 'en')
    
    questions = [
        "Briefly describe this image.",
        "Summarize this image in a few words."
    ]
    
    converted_data = dataframe_to_format(df, questions, args.img_root)
    save_to_json(converted_data, args.output_file)
    print(f"Converted data has been saved to {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert LAION5B dataframe to instruction tuning dataset format.")
    parser.add_argument('input_file', type=str, help="Path to the CSV file containing LAION5B metadata")
    parser.add_argument('img_root', type=str, help="Root directory path for LAION5B images")
    parser.add_argument('output_file', type=str, help="Output file path for the converted JSON data")
    
    args = parser.parse_args()
    main(args)
