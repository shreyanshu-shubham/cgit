#!/usr/bin/env python3

import argparse
import os
import util
from pathlib import Path

def main():
     parser = argparse.ArgumentParser()
     
     commands = parser.add_subparsers(dest="command",required=True)

     find_root_parser = commands.add_parser("find-root")
     find_root_parser.add_argument('-d',required=False,action="store",help="path for which to find cgit root",dest="directory",default=os.path.abspath(os.curdir))

     init_parser = commands.add_parser("init")
     init_parser.add_argument("path", help="path to directory to initialize as a cgit repository",default=os.getcwd())

     hash_object_parser = commands.add_parser('hash-object')
     hash_object_parser.add_argument('-w',"--write",required=False,action="store_true",help="Write it in the repository")
     hash_object_parser.add_argument('-t',"--type",required=False,action="store",choices=["blob","tree","commit"],help="Type of hash object",default="blob")
     hash_object_parser_input = hash_object_parser.add_mutually_exclusive_group(required=True)
     hash_object_parser_input.add_argument('-stdin',action="store_true",help="Read content from standard in")
     hash_object_parser_input.add_argument('files',action="store",nargs=argparse.REMAINDER,help="Get hash for content for this file")

     cat_file_parser = commands.add_parser("cat-file")
     cat_file_parser.add_argument("object",metavar="sha1hash")
     cat_file_parser_flags = cat_file_parser.add_mutually_exclusive_group(required=True)
     cat_file_parser_flags.add_argument('-p',required=False,action="store_true",help="print the content of the object")
     cat_file_parser_flags.add_argument('-t',required=False,action="store_true",help="print the type of the object")

     write_tree_parser = commands.add_parser("write-tree")
     
     ARGS = parser.parse_args()
     print(ARGS)
     
     match ARGS.command:
          # case "add"          : cmd_add(ARGS)
          # case "check-ignore" : cmd_check_ignore(ARGS)
          # case "checkout"     : cmd_checkout(ARGS)
          # case "commit"       : cmd_commit(ARGS)
          # case "log"          : cmd_log(ARGS)
          # case "ls-files"     : cmd_ls_files(ARGS)
          # case "ls-tree"      : cmd_ls_tree(ARGS)
          # case "rev-parse"    : cmd_rev_parse(ARGS)
          # case "rm"           : cmd_rm(ARGS)
          # case "show-ref"     : cmd_show_ref(ARGS)
          # case "status"       : cmd_status(ARGS)
          # case "tag"          : cmd_tag(ARGS)
          # case "write-tree"   : cmd_write_tree(ARGS)
          case "cat-file": 
               util.cat_file(ARGS.object,ARGS.t,ARGS.t)
          case "hash-object":
               util.hash_object(ARGS.type,ARGS.write,ARGS.stdin,ARGS.files)
          case "init"         : 
               util.init_repo(Path(ARGS.path))
          # custom commands
          case "find-root": 
               print(util.get_cgit_root(Path(ARGS.directory)))

def util_write_tree(dir_path: str):
     hash_list = []
     for e in os.scandir(dir_path):
          if e.name == ".cgit":
               continue
          full_path = os.path.join(dir_path,e.name)
          object_type = ""
          sha1_hash = ""
          if e.is_file(follow_symlinks=False):
               object_type="blob"
               with open(full_path,"rb") as f:
                    data = f.read()
               sha1_hash = util_hash_object(content=data,write=True)
          elif e.is_dir(follow_symlinks=False):
               object_type="tree"
               sha1_hash = util_write_tree(full_path)
          hash_list.append((object_type,sha1_hash,e.name))
     tree = ''.join (f'{objt} {shash} {name}\n' for objt, shash, name in sorted (hash_list))
     return util_hash_object(tree.encode(),object_type="tree",write=True)

def cmd_write_tree(ARGS:argparse.Namespace):
     cgit_root = util_find_root()
     if cgit_root:
          util_write_tree(cgit_root)
     else:
          print_error("could not find a cgit repository")

if __name__ == '__main__':
     main()