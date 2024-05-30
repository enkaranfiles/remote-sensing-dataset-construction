from datasets import load_dataset, DatasetDict
from huggingface_hub import HfApi, HfFolder
import os

def save_token():
    Hf = HfFolder()
    Hf.save_token("#YOUR_TOKEN_HERE")
    return Hf.get_token()

def upload_json_dataset(path_to_json_dir, repo_name, token):
    json_files_pattern = os.path.join(path_to_json_dir, '*.json')
    dataset = load_dataset('json', data_files=json_files_pattern)
    
    if not isinstance(dataset, DatasetDict):
        dataset = DatasetDict({'train': dataset})
    
    dataset.push_to_hub(repo_name, token=token)

def upload_zip_file(zip_file_path, repo_name, token):
    api = HfApi()
    api.upload_file(
        token=token,
        repo_id=repo_name,
        repo_type='dataset',
        path_in_repo="dataset.zip",  # ensure file name is used in the repo
        path_or_fileobj=zip_file_path
    )

def main():
    token = save_token()
    print(token)
    repo_name = '#REPO_NAME'
    path_to_json_dir = '#PATH_TO_JSON_DIR'
    zip_file_path = '#PATH_TO_ZIP_FILE'
    
    # Uncomment to upload JSON dataset
    # upload_json_dataset(path_to_json_dir, repo_name, token)
    
    # Uncomment to upload zipped directory
    upload_zip_file(zip_file_path, repo_name, token)
    
    print("Upload completed successfully.")

if __name__ == "__main__":
    main()
