import json
import random
import argparse

# Function to load JSON data from a file
def load_json_data(json_file_path):
    with open(json_file_path, 'r') as f:
        return json.load(f)

# Function to convert captioning dataset to QA format
def convert_captioning_dataset_to_qa_format(dataset, image_path_prefix):
    questions = [
        "Briefly describe this image.",
        "Summarize this image in a few words."
    ]

    new_format_data = []
    for image in dataset["images"]:
        for sentence in image["sentences"]:
            question = random.choice(questions)  # Randomly choose a question
            new_entry = {
                "id": str(sentence["sentid"]),
                "image": f"{image_path_prefix}{image['filename']}",  # Prepend path
                "conversations": [
                    {
                        "from": "human",
                        "value": f"<image>\n{question}"
                    },
                    {
                        "from": "gpt",
                        "value": sentence["raw"]
                    }
                ]
            }
            new_format_data.append(new_entry)

    return new_format_data

# Function to save data to a JSON file
def save_to_json(data, output_file_path):
    with open(output_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Main function
def main(args):
    captioning_data = load_json_data(args.json_file_path)
    converted_data = convert_captioning_dataset_to_qa_format(captioning_data, args.image_path_prefix)
    save_to_json(converted_data, args.output_file_path)
    print(f"Converted data has been saved to {args.output_file_path}")

# Command-line argument parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert captioning dataset to instruction tuning dataset format.")
    parser.add_argument('json_file_path', type=str, help="Path to the JSON file containing captioning data")
    parser.add_argument('image_path_prefix', type=str, help="Prefix path to the images")
    parser.add_argument('output_file_path', type=str, help="Output file path for the converted JSON data")

    args = parser.parse_args()
    main(args)
