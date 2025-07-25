def parse(gitignore_filepath):
    with open(gitignore_filepath,"r") as f:
        ignore_rules = f.read().split()
    
    # remove empty lines
    ignore_rules = [ f for f in ignore_rules if str(f).trim() != '' ]

    # remove commented lines 
    ignore_rules = [ f for f in ignore_rules if not str(f).startswith("#") ]

    

"""
PATTERN FORMAT

    A line starting with # serves as a comment. Put a backslash ("\") in front of the first hash for patterns that begin with a hash.

    Trailing spaces are ignored unless they are quoted with backslash ("\").

    An optional prefix "!" which negates the pattern; any matching file excluded by a previous pattern will become included again. It is not possible to re-include a file if a parent directory of that file is excluded. Git doesn’t list excluded directories for performance reasons, so any patterns on contained files have no effect, no matter where they are defined. Put a backslash ("\") in front of the first "!" for patterns that begin with a literal "!", for example, "\!important!.txt".

    If there is a separator at the end of the pattern then the pattern will only match directories, otherwise the pattern can match both files and directories.

    An asterisk "*" matches anything except a slash. The character "?" matches any one character except "/". The range notation, e.g. [a-zA-Z], can be used to match one of the characters in a range. See fnmatch(3) and the FNM_PATHNAME flag for a more detailed description.

    Two consecutive asterisks ("**") in patterns matched against full pathname may have special meaning:

        A leading "**" followed by a slash means match in all directories. For example, "**/foo" matches file or directory "foo" anywhere, the same as pattern "foo". "**/foo/bar" matches file or directory "bar" anywhere that is directly under directory "foo".

        A trailing "/**" matches everything inside. For example, "abc/**" matches all files inside directory "abc", relative to the location of the .gitignore file, with infinite depth.

        A slash followed by two consecutive asterisks then a slash matches zero or more directories. For example, "a/**/b" matches "a/b", "a/x/b", "a/x/y/b" and so on.
"""