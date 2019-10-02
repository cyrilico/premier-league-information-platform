import os

filename = '16-17.json'
with open(filename, 'rb+') as f:
    f.seek(-1, os.SEEK_END)
    f.truncate()

with open(filename, 'a') as f:
    f.write(']')