#!/usr/bin/env python3
import os
import sys


if len(sys.argv) >= 2:
    directory = str(sys.argv[1])
else:
    directory = os.path.dirname(os.path.realpath(__file__))
    print('No directory given! Using current working directory: ', directory)


for root, dirs, files in os.walk(directory):
    print('**', root)
    for file in files:
        pathname = os.path.join(root, file)
        if os.path.exists(pathname):
            print(pathname)
