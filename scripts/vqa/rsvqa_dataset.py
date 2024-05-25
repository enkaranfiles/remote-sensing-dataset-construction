import json
import argparse
import os

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def convert_to_instruction_tuning_format(questions, answers):
    instruction_tuning_dataset = {"annotations": []}
    answers_by_id = {answer["id"]: answer for answer in answers["answers"]}
    
    for question in questions["questions"]:
        if question["active"]:
            filename = f'{question["img_id"]}.png'
            qa_pairs = []
            
            for answer_id in question["answers_ids"]:
                if answer_id in answers_by_id:
                    answer = answers_by_id[answer_id]
                    if answer["active"]:
                        qa_pairs.append({
                            "question": question["question"],
                            "answer": answer["answer"],
                            "type": question["type"]
                        })
            
            instruction_tuning_dataset["annotations"].append({
                "filename": filename,
                "qa_pairs": qa_pairs
            })
                        
    return instruction_tuning_dataset

def convert_dataset_to_required_format(dataset):
    converted_data = {}
    
    for item in dataset:
        image_id = item['filename'].rsplit('.', 1)[0]  # Extract filename without extension
        image_path = f"{image_id}.png"  # Convert to PNG and construct storage path
        
        if image_id not in converted_data:
            converted_data[image_id] = {
                "id": image_id,
                "image": image_path,
                "conversations": []
            }
        
        for qa_pair in item['qa_pairs']:
            converted_data[image_id]['conversations'].append({"from": "human", "value": "<image>\n" + qa_pair['question']})
            converted_data[image_id]['conversations'].append({"from": "gpt", "value": qa_pair['answer']})

    return list(converted_data.values())

def convert_dataset_format(original_datasets):
    new_format = []
    
    for dataset in original_datasets:
        for i in range(0, len(dataset["conversations"]), 2):
            entry = {
                "id": dataset["id"],
                "image": dataset["image"],
                "conversations": [dataset["conversations"][i], dataset["conversations"][i+1]]
            }
            new_format.append(entry)
    
    return new_format

def main(args):
    questions = load_json_data(args.questions_file)
    answers = load_json_data(args.answers_file)
    
    instruction_tuning_dataset = convert_to_instruction_tuning_format(questions, answers)
    converted_dataset = convert_dataset_to_required_format(instruction_tuning_dataset['annotations'])
    final_format_dataset = convert_dataset_format(converted_dataset)
    
    with open(args.output_file, 'w') as f:
        json.dump(final_format_dataset, f, indent=4)
    
    print(f"Converted data has been saved to {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert VQA dataset to instruction tuning dataset format.")
    parser.add_argument('questions_file', type=str, help="Path to the JSON file containing questions data")
    parser.add_argument('answers_file', type=str, help="Path to the JSON file containing answers data")
    parser.add_argument('output_file', type=str, help="Output file path for the converted JSON data")
    
    args = parser.parse_args()
    main(args)
