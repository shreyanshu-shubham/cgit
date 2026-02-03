# these are temp function before actual integrations

import os
import sys
import zlib
import hashlib
from pathlib import Path
import constants

def print_error(text:str,error_code:int=1) -> None:
     print(text,file=sys.stderr)
     exit(error_code)

def get_cgit_root(current_directory:Path) -> str|None:
    while True:
        cgit_dir:Path = current_directory / constants.data_dir_name
        if cgit_dir.is_dir():
            return current_directory
        elif current_directory == current_directory.parent:
            return None
        else:
            current_directory = current_directory.parent

def is_in_cgit_repo(directory:Path) -> bool:
    return get_cgit_root(directory) is not None

def init_repo(base_dir: Path) -> None:
    if not base_dir.exists():
        if not base_dir.parent.exists():
            print_error(f"the following path does not exists: {base_dir.parent.absolute()}\ncannot initialize the project: {base_dir.name}")
        base_dir.mkdir()

    cgit_dir:Path = base_dir / ".cgit"
    if cgit_dir.exists() and cgit_dir.is_dir():
        print_error("the given path already a cgit repository")
    elif is_in_cgit_repo(base_dir):
        print_error("the given path is already in cgit repository")

    cgit_dir.mkdir()
    for name,details in constants.default_data_dir_structure.items():
        match details.get("type"):
            case "directory":
                (cgit_dir / name).mkdir(parents=True)
            case "file":
                file_path:Path = cgit_dir / details.get("path")
                file_path.parent.mkdir(parents=True,exist_ok=True)
                with file_path.open("w") as f:
                    f.write(details.get("content"))
    print(f"Initialized empty cgit repository in {cgit_dir}")

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
