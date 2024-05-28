from datasets import load_dataset

from huggingface_hub import HfFolder

Hf = HfFolder()
Hf.save_token("#TOKEN")

path_to_json_dir = '#PATH_TO_JSON_DIR'

dataset = load_dataset('json', data_files=f'{path_to_json_dir}/*.json')

dataset.push_to_hub('#REPO', token=True)
