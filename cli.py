#!/usr/bin/env python3

import argparse
import hashlib
import os
import sys
import util

def main():
     parser = argparse.ArgumentParser()
     
     commands = parser.add_subparsers(dest="command",required=True)

     init_parser = commands.add_parser("init")
     init_parser.add_argument("path", nargs="?", default=os.getcwd())

     hash_object_parser = commands.add_parser('hash-object')
     hash_object_parser.add_argument('file',nargs="?",help="Get hash for content for this file")
     hash_object_parser.add_argument('-w',required=False,action="store_true",help="Write it in the repository")
     hash_object_parser.add_argument('-t',required=False,action="store",choices=["blob","tree","commit"],help="Type of hash",default="blob")
     hash_object_parser.add_argument('-stdin',required=False,action="store_true",help="Read content from standard in")

     find_root_parser = commands.add_parser("find-root")
     find_root_parser.add_argument('-d',required=False,action="store",help="absolute path for which to find cgit root",dest="directory",default=os.path.abspath(os.curdir))

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
          case "cat-file"     : util.cat_file(ARGS.object,ARGS.t,ARGS.t)
          # case "check-ignore" : cmd_check_ignore(ARGS)
          # case "checkout"     : cmd_checkout(ARGS)
          # case "commit"       : cmd_commit(ARGS)
          # case "hash-object"  : cmd_hash_object(ARGS)
          case "init"         : util.init_repo(ARGS.path)
          # case "log"          : cmd_log(ARGS)
          # case "ls-files"     : cmd_ls_files(ARGS)
          # case "ls-tree"      : cmd_ls_tree(ARGS)
          # case "rev-parse"    : cmd_rev_parse(ARGS)
          # case "rm"           : cmd_rm(ARGS)
          # case "show-ref"     : cmd_show_ref(ARGS)
          # case "status"       : cmd_status(ARGS)
          # case "tag"          : cmd_tag(ARGS)
          # case "write-tree"   : cmd_write_tree(ARGS)
          # custom commands
          case "find-root"    : print(util.get_cgit_root(ARGS.directory))
          case _              : util.print_error("Bad cgit command.")

def cmd_add(): pass
def cmd_check_ignore(): pass
def cmd_checkout(): pass
def cmd_commit(): pass
def cmd_log(): pass
def cmd_ls_files(): pass
def cmd_ls_tree(): pass
def cmd_rev_parse(): pass
def cmd_rm(): pass
def cmd_show_ref(): pass
def cmd_status(): pass
def cmd_tag(): pass

def util_hash_object(content:bytes, object_type:str = "blob", write:bool = False) ->  str:
     
     content = object_type.encode() + b'\x00' + content
     sha1_hash = hashlib.sha1(content).hexdigest()
     if write:
          repo_root = util_find_root()
          if repo_root:
               sha_dir = os.path.join(repo_root,".cgit","objects",sha1_hash[:2])
               sha_file = os.path.join(repo_root,".cgit","objects",sha1_hash[:2],sha1_hash[2:])
          else:
               print_error("current dir is not a cgit repository")
          
          os.makedirs(sha_dir,exist_ok=True)
          with open(sha_file,"wb") as f:
               f.write(content)
     return sha1_hash

def cmd_hash_object(ARGS):
     if ARGS.stdin:
          content = input().encode()
     else:
          with open(ARGS.file,"rb") as f:
               content = f.read()
     print(util_hash_object(content=content,object_type=ARGS.t,write=ARGS.w))

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