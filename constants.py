from typing import Dict

data_dir_name:str = ".cgit"

file_content_config:str = """[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
	ignorecase = true
"""

file_content_description:str = """Unnamed repository; edit this file 'description' to name the repository.
"""

file_content_exclude:str = """# git ls-files --others --exclude-from=.git/info/exclude
# Lines that start with '#' are comments.
# For a project mostly in C, the following would be a good set of
# exclude patterns (uncomment them if you want to use them):
# *.[oa]
# *~
"""

file_content_head:str = """ref: refs/heads/master
"""

default_data_dir_structure:Dict[str,Dict] = {
	"hooks": {"type": "directory"},
	"info": {"type": "directory"},
	"objects/info": {"type": "directory"},
	"objects/pack": {"type": "directory"},
	"refs/heads": {"type": "directory"},
	"refs/tags": {"type": "directory"},
    
	"config":{"type":"file","path":"config","content":file_content_config},
	"description": {"type":"file","path":"description","content":file_content_description},
	"HEAD": {"type":"file","path":"HEAD","content":file_content_head},
	"exclude": {"type":"file","path":"info/exclude","content":file_content_exclude},
    # TODO : add default hooks file creation
}
