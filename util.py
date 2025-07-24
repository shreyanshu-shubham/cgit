# these are temp function before actual integrations

import os

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

def create_file_blob(cgit_path, file_path):
    pass

def create_tree(cgit_path):
    pass

def create_commit(cgit_path):
    pass
