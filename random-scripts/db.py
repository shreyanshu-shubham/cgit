import sqlite3
import os

index_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"test",".cgit/index.db"))
print(index_file)
with sqlite3.connect(index_file) as conn:
    cur = conn.cursor()
    cur.execute("create table file_index( ctime integer not null, mtime integer not null, mode integer not null, file_size_bytes integer not null, sha1hash text not null, file_path text not null);")


