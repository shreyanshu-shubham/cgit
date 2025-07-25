# these are temp function before actual integrations

import os
import sys
import shutil
import zlib
import hashlib
from utility import gitignore_to_regex

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

def cat_file(sha1hash,flag_type,flag_print) -> None:
    cgit_root = get_cgit_root(os.path.abspath(os.curdir))
    if not cgit_root:
        print_error("not within a cgit repository")
    object_file = os.path.join(cgit_root,".cgit/objects",sha1hash[:2],sha1hash[2:])
    if not os.path.exists(object_file):
        print_error("the object does  not exists")
    with open(object_file,"rb") as f:
        uncompressed_data = zlib.decompress(f.read()).decode()
    if flag_print:
        print(uncompressed_data.split("\x00")[-1])
    if flag_type:
        print(uncompressed_data.split("\x00")[0].split(" ")[0])

def hash_object(content:str,object_type:str ,write_to_repo:bool=False) -> None:
    content = f"{object_type} {len(content)}\x00{content}".encode()
    sha1hash = hashlib.sha1(content).hexdigest()
    if write_to_repo:
        cgit_root = get_cgit_root(os.path.abspath(os.curdir))
        if not cgit_root:
            print_error("not within a cgit repository")
        os.makedirs(os.path.join(cgit_root,".cgit/objects",sha1hash[:2]))
        with open(os.path.join(cgit_root,".cgit/objects",sha1hash[:2],sha1hash[2:]),"wb") as f:
            f.write(zlib.compress(content))
    print(sha1hash)

def get_ignore_list():
    gitignore_to_regex.parse()