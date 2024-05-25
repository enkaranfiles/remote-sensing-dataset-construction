import json
import os
import argparse

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def convert_rsvqaxbe_format(questions, answers, root_path):
    active_answers = {ans['question_id']: ans['answer'] for ans in answers if ans['active']}
    
    new_format_data = [
        {
            "id": str(question['id']),
            "image": f"{root_path}{question['img_id']}.tiff",
            "conversations": [
                {
                    "from": "human",
                    "value": f"<image>\n{question['question']}"
                },
                {
                    "from": "gpt",
                    "value": active_answers.get(question['id'], "Unknown")
                }
            ]
        }
        for question in questions if question['active'] and question['id'] in active_answers
    ]
    
    return new_format_data

def save_to_json(data, output_file_path):
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def main(args):
    questions = load_json_data(args.questions_file)
    answers = load_json_data(args.answers_file)
    
    converted_data = convert_rsvqaxbe_format(questions['questions'], answers['answers'], args.img_root)
    save_to_json(converted_data, args.output_file)
    print(f"Converted data has been saved to {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert RSVQAxBEN dataset to instruction tuning dataset format.")
    parser.add_argument('questions_file', type=str, help="Path to the JSON file containing RSVQAxBEN questions data")
    parser.add_argument('answers_file', type=str, help="Path to the JSON file containing RSVQAxBEN answers data")
    parser.add_argument('img_root', type=str, help="Root directory path for RSVQAxBEN images")
    parser.add_argument('output_file', type=str, help="Output file path for the converted JSON data")
    
    args = parser.parse_args()
    main(args)
