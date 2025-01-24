# Template: File Automation Script
import os
import shutil

def organize_files(source_dir, destination_dir):
    for file_name in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, file_name)):
            ext = file_name.split('.')[-1]
            ext_dir = os.path.join(destination_dir, ext)
            os.makedirs(ext_dir, exist_ok=True)
            shutil.move(os.path.join(source_dir, file_name), ext_dir)

# Example Usage
source_directory = "source"
destination_directory = "organized"
organize_files(source_directory, destination_directory)
