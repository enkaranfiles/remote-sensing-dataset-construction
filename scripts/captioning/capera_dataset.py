import json
import os
import random
import argparse

def load_json_data(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)['ERA_caption']

def create_question(caption):
    questions = [
        "Briefly describe this image.",
        "Summarize this image in a few words."
    ]
    question_template = random.choice(questions)
    return f"<image>\n{question_template}"

def convert_data(caption_data, base_dir):
    converted_data = []
    for item in caption_data:
        video_id = item['video_id']
        captions = item['annotation']['English_caption']
        
        sport_type = video_id.split('_')[0]
        sport_dir = os.path.join(base_dir, sport_type)
        image_filename = f"{video_id.split('.')[0]}.png"
        image_path = os.path.join(sport_dir, image_filename)
        
        if os.path.exists(image_path):
            for caption in captions:
                new_entry = {
                    "id": video_id.split('.')[0],
                    "image": image_path,
                    "conversations": [
                        {
                            "from": "human",
                            "value": create_question(caption)
                        },
                        {
                            "from": "gpt",
                            "value": caption
                        }
                    ]
                }
                converted_data.append(new_entry)
    return converted_data

def save_to_json(data, output_file_path):
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def main(args):
    caption_data = load_json_data(args.json_file_path)
    converted_data = convert_data(caption_data, args.base_dir)
    save_to_json(converted_data, args.output_file_path)
    print(f"Converted data has been saved to {args.output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert captioning data to instruction tuning dataset format.")
    parser.add_argument('json_file_path', type=str, help="Path to the JSON file containing caption data")
    parser.add_argument('base_dir', type=str, help="Base directory for images")
    parser.add_argument('output_file_path', type=str, help="Output file path for the converted JSON data")

    args = parser.parse_args()
    main(args)
