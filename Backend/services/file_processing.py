
import os
import shutil
import zipfile
from pathlib import Path
from typing import List, Dict

TEMP_DIR = "temp_uploads"

def ensure_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

def save_upload_file(upload_file, filename: str) -> str:
    ensure_temp_dir()
    file_path = os.path.join(TEMP_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def extract_zip(zip_path: str, extract_to: str):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def get_file_structure(root_dir: str) -> Dict:
    file_list = []
    tree_str = ""
    
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            file_list.append(os.path.join(root, f))
            tree_str += f"{subindent}{f}\n"
            
    return {
        "root": root_dir,
        "files": file_list,
        "tree": tree_str
    }

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return "<Binary file or encoding error>"
    except Exception as e:
        return f"<Error reading file: {str(e)}>"

def cleanup_temp_files(dir_path: str):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
