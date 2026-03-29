import os
import sys

FILE_SUFFIX = ".cpp"
IGNORE_LIST = {"test",".git","leet"}

def Search_recursive_entries(source_folder : str, ignorelist : set)->list:
    cpp_paths =[]
    for entry in os.scandir(source_folder):
        if any(keyword in entry.name.lower() for keyword in ignorelist):
            continue
        if entry.is_dir():
            cpp_paths.extend(Search_recursive_entries(entry.path,IGNORE_LIST))
        elif entry.is_file() and entry.name.lower().endswith(FILE_SUFFIX):
            cpp_paths.append(entry.path)
    return cpp_paths

def find_cpp_files(source_folder: str) -> list:
    cpp_paths = []
    cpp_paths = Search_recursive_entries(source_folder,IGNORE_LIST)
    return cpp_paths


def main(source: str,) -> list:
    if not os.path.isdir(source):
        raise Exception(f"Folder not found: {source}")

    cpp_files = find_cpp_files(source)
    for cpp_file_path in cpp_files:
        print(cpp_file_path)
        
    return cpp_files


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("Usage: python cppcompiler.py <folder_path>")
    source = args[1]

    main(source)
