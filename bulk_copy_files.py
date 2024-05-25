import os
import shutil
import argparse

def copy_image_files(source_roots, target_directory):
    """
    Copies all image files from a list of nested directory structures to a single flat directory target_directory.
    
    Args:
    source_roots (list): List of root directories from which to start searching for image files.
    target_directory (str): The directory to which all image files should be copied.
    
    Returns:
    int: The count of files successfully copied.
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.tif'}  
    copied_files_count = 0  # Counter for the number of files copied
    
    for source_root in source_roots:
        # Walk through all directories and files in each source_root
        for dirpath, dirnames, filenames in os.walk(source_root):
            for file in filenames:
                try:
                    if os.path.splitext(file)[1].lower() in image_extensions:
                        source_path = os.path.join(dirpath, file)
                        target_path = os.path.join(target_directory, file)
                        
                        # Copy file to target_directory, handle potential overwrites
                        if not os.path.exists(target_path):
                            shutil.copy(source_path, target_path)
                            copied_files_count += 1
                        else:
                            # Handling file name conflict by renaming
                            base, extension = os.path.splitext(file)
                            counter = 1
                            new_file = f"{base}_{counter}{extension}"
                            new_target_path = os.path.join(target_directory, new_file)
                            while os.path.exists(new_target_path):
                                counter += 1
                                new_file = f"{base}_{counter}{extension}"
                                new_target_path = os.path.join(target_directory, new_file)
                            shutil.copy(source_path, new_target_path)
                            copied_files_count += 1
                except Exception as e:
                    print(f"Error copying {file}: {e}")

    return copied_files_count

def main(args):
    source_roots = args.source_roots.split(',')
    copied_files_count = copy_image_files(source_roots, args.target_directory)
    print(f"{copied_files_count} files have been copied to {args.target_directory}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy image files from multiple source directories to a single target directory.")
    parser.add_argument('source_roots', type=str, help="Comma-separated list of source directories.")
    parser.add_argument('target_directory', type=str, help="Target directory to copy the images to.")
    
    args = parser.parse_args()
    main(args)
