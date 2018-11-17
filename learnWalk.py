#!/usr/bin/env python3
import os
import sys

if len(sys.argv) >= 2:
    directory = str(sys.argv[1])
else:
    print('Not enough arguments!')
    sys.exit(0)

for root, dirs, files in os.walk(directory):
    print('**', root)
    for file in files:
        pathname = os.path.join(root, file)
        if os.path.exists(pathname):
            print(pathname)
