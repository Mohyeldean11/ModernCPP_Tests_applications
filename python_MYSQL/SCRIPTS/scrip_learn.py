import os
import json
import shutil
from subprocess import PIPE , run
import sys

Dir_pattern = "game"


def find_all_dirs(source)->list:
    paths = []
    for root,dirs,files in os.walk(source):
        
        for directory in dirs:
            if Dir_pattern in  directory.lower():
                path = os.path.join(source,directory)
                paths.append(path)
        break
    return path

def copy_path(source,dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source,dest)


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_name_from_paths(paths,to_strip)->list:
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip,"")
        new_names.append(new_dir_name)
    return new_names

def main(source,target)->None:
    cwd = os.getcwd()
    source_path = os.path.join(cwd,source)
    target_path = os.path.join(cwd,target)

    path = find_all_dirs(source= source_path)
    print(path)

def make_json_metadate(path,dirs):
    data = {
        "names" : dirs,
        "number of dirs" : len(dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)
        
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("you must pass a source and a target directory - only")
    
    source,target = args[1:]