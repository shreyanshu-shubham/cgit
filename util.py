# these are temp function before actual integrations

import constants

import os
import sys
import zlib
import hashlib
from pathlib import Path
from typing import List, Dict

def print_error(text:str,error_code:int=1) -> None:
     print(text,file=sys.stderr)
     exit(error_code)

def get_cgit_root(current_directory:Path) -> Path|None:
    while True:
        cgit_dir:Path = current_directory / constants.data_dir_name
        if cgit_dir.is_dir():
            return current_directory
        elif current_directory == current_directory.parent:
            return None
        else:
            current_directory = current_directory.parent

def get_cgit_directory(current_dir:Path) -> Path|None:
    cgit_root = get_cgit_root(current_dir)
    if not current_dir:
        return None
    return cgit_root/constants.data_dir_name

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

def hash_object_helper(content:str,object_type:str ,write_to_repo:bool=False) -> str:
    content = f"{object_type} {len(content)}\x00{content}".encode()
    sha1hash:str = hashlib.sha1(content).hexdigest()
    if write_to_repo:
        cgit_dir = get_cgit_directory(Path(os.curdir))
        if not cgit_dir:
            print_error("not within a cgit repository")
        object_base_dir = cgit_dir / "objects" / sha1hash[:constants.hash_object_level_1_size]
        object_file_path= object_base_dir / sha1hash[constants.hash_object_level_1_size:]
        if not object_base_dir.exists():
            object_base_dir.mkdir()
        with object_file_path.open("wb") as f:
            f.write(zlib.compress(content))
    return sha1hash

def hash_object(object_type:str, write:bool= False, stdin:bool = False, files:List|None = None) -> None:
    if stdin:
        content:str = input()
        print(hash_object_helper(content=content,object_type=object_type,write_to_repo=write))
        return
    longest_file_name:int = 0
    file_hash_map:Dict[str,str] = dict()
    for fl in files:
        file_path:Path = Path(fl)
        longest_file_name = max(longest_file_name,len(fl))
        if not file_path.exists() :
            file_hash_map[fl] = "does not exists"
        elif not file_path.is_file():
            file_hash_map[fl] = "is not a file"
        else:
            file_hash_map[fl] = hash_object_helper(file_path.read_text(),object_type,write)
    for fl,hash_value in file_hash_map.items():
        print(f"{fl.ljust(longest_file_name+2,".")}: {hash_value}")

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

