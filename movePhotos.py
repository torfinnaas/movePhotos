#!/usr/bin/env python3
import os
import sys
import PIL.Image
import PIL.ExifTags
import shutil
from datetime import datetime



VERSION='0.0.0.1'
EXIF_DATETIME_TAG=36867
NEW_PATH_PREFIX='/home/torfinn/tmp'
#'2016:03:25 21:29:36'
DATETIME_PATTERN='%Y:%m:%d %H:%M:%S'



def isPhotoFile(fileExtension):
    photoExtensions = [".jpg", ".jpeg", ".png"]
    if fileExtension in photoExtensions:
        return True
    else:
        return False


print('movePhotos version', VERSION)

if len(sys.argv) >= 2:
    directory = str(sys.argv[1])
else:
    directory = os.path.dirname(os.path.realpath(__file__))
    print('No directory given! Using current working directory: ', directory)


for root, dirs, files in os.walk(directory):
#    print('**', root)d
    for file in files:
        pathname = os.path.join(root, file)
        filename, file_extension = os.path.splitext(pathname)
        if os.path.exists(pathname) and isPhotoFile(file_extension):
            if file_extension == '.jpg' or file_extension == '.jpeg':
                img = PIL.Image.open(pathname)
                exif_data = img._getexif()
                dateTimeStr = exif_data.get(EXIF_DATETIME_TAG)
                # print(pathname, dateTimeStr)
                datetime: datetime = datetime.strptime(dateTimeStr, DATETIME_PATTERN)
                year = datetime.year
                month = datetime.month
            if file_extension == '.png':
                print('PNG format not supported yet!')
                year = 2018
                month = 7

            # Move/copy the file
            newpathname = NEW_PATH_PREFIX + '/' + str(year) + '/' + str(month) + '/' + filename + file_extension;
            print('Copies from: ', pathname, ' ==> to : ', newpathname)
            #shutil.copyfile(pathname, newpathname)



