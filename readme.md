# cgit
a little not so capable younger brother of git

### commands done
* find-root
    * if `-d` absolute path is provided else from the current working dir give the root of the cgit repo
* init
    * if `path` absolute path is provided that dir will be init else the current dir
* hash-object
    * -t --type : commit, tree, blob 
    * -w --write: write the changes to object database
    * -stdin : use the input from the terminal, ignore the files
    * files: files to generate hash object for the provided files
* cat-file
### commands todo
* add
    * pathlist/filelist
    * -n --dry-run
    * -v --verbose
    * -f --force : to add ignored files
    * -p --patch : add huck instead of whole files
* check-ignore : check if given file is ignored
    * -q --quite : only a exit code for single file
    * --stdin : file paths from stdin, one file per 
* checkout 
    * `NOTE : not implemeting it to focus on switch`
* switch
    * git switch <existing-branch>
    * git switch -c|-C <new-branch>
    * git switch -c|-C <new-branch> [<starting-point>]
* commit
    * -m --message : commit message
    * --amend
    * --no-edit
* log
    * --graph
    * --oneline
* ls-files : show working tree and indexed files
    * no-flags : show all working tree and indexed files
    * -d --deleted : show deleted
    * -m --modified : show modified
    * -o --others : untracked or ignored
* ls-tree
    * git ls-tree [-r|--recursive] [--name-only] <branch_name/commit_hash>
        * -r|--recursive : recurse into subtree
        * --name-only : only the file name and to the mode, objtype and objhash 
* rev-parse
    * git rev-parse branch_name : Get the commit hash of a branch:
    * git rev-parse --show-toplevel : get commit hash and root dir path
* rm
    * file/dir list
    * -r --recursice : to delete dir
* show-ref
    * git show-ref : Show all refs in the repository:
    * git show-ref --branches : Show only heads references:
    * git show-ref --tags : Show only tags references:
* status
    * output format
        * --long
        * --short
* tag
    * -a --anotate
    * -l --list
    * -d --delete
    * -e --edit
    * -m --message
* write-tree
    * git write-tree : Create a tree object from the current index:
* branch
    * -m --move : rename branch
    * -c --copy : copy branch
    * -l --list : list local branch optionally takes regex to match
        * defaults to local
        * -a : list all branch
        * -r : list remote branch
* restore
    * file/dir list to restore to last commit
* reset
    * --hard
    * --mixed
    * --soft
        * optionally only file or path to restore
        * HEAD~n : commit range from head range 
        * commit : commit to restore to 
