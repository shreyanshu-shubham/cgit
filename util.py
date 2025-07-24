# these are temp function before actual integrations

import os
import sys
import shutil

def print_error(text:str,error_code:int=1) -> None:
     print(text,file=sys.stderr)
     exit(error_code)

def get_cgit_root(current_directory) -> str|None:
    parent_directory = os.path.realpath(os.path.join(current_directory,".."))
    while current_directory != parent_directory:
        if os.path.isdir(os.path.join(current_directory,".cgit")):
            return current_directory
        current_directory = parent_directory
        parent_directory = os.path.realpath(os.path.join(current_directory,".."))
    return None

def is_in_cgit_repo(directory):
    return get_cgit_root(directory) is not None

def init_repo(base_dir):
    if not os.path.exists(base_dir):
        print_error(f"the following path does not exists: {base_dir}")
    elif not os.path.isdir(base_dir): 
        print_error(f"the given path is not a directory : {base_dir}")
    elif os.path.exists(os.path.join(base_dir,".cgit")) and os.path.isdir(os.path.join(base_dir,".cgit")):
        print_error(f"the given path already a cgit repository")
    elif is_in_cgit_repo(base_dir):
        print_error(f"the given path is already in cgit repository")

    repo_path=os.path.join(base_dir,".cgit")

    dir_to_create = [
        "hooks",
        "info",
        "objects/info",
        "objects/pack",
        "refs/heads",
        "refs/tags",
    ]

    files_to_create = {
        "config":"config",
        "description":"description",
        "HEAD":"HEAD",
        "info/exclude":"exclude",
        # TODO : add default hooks file creation
    }

    for d in dir_to_create:
        os.makedirs(os.path.join(repo_path,d),exist_ok=True)
    for f,fc in files_to_create.items():
        shutil.copy(
            src=os.path.join(os.path.dirname(os.path.realpath(os.path.abspath(__file__))),"default",fc),
            dst=os.path.join(repo_path,f)
        )
    print(f"Initialized empty cgit repository in {repo_path}")

def create_file_blob(cgit_path, file_path):
    pass

def create_tree(cgit_path):
    pass

def create_commit(cgit_path):
    pass
