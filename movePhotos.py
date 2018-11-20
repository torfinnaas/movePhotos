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
# Date/time format in EXIF data from jpeg files: '2016:03:25 21:29:36'
DATETIME_PATTERN='%Y:%m:%d %H:%M:%S'



def isPhotoFile(fileExtension):
    photoExtensions = [".jpg", ".jpeg", ".png"]
    if fileExtension in photoExtensions:
        return True
    else:
        return False


def initial():
    print('MovePhotos version', VERSION)

    src_dir = os.path.dirname(os.path.realpath(__file__))

    if len(sys.argv) != 2:
        print(f'Usage: {__name__} <destiantion directory>')
        sys.exit(0)
        #dest_dir = NEW_PATH_PREFIX
    else:
        dest_dir = str(sys.argv[1])
        print('Moving files from {} to {}'.format(src_dir, dest_dir))

    return (src_dir, dest_dir)




def traversDirectories(src_dir, dest_dir):
    for root, dirs, files in os.walk(src_dir):
        print(f'Directory: {root}:')
        for file in files:
            pathname = os.path.join(root, file)
            temp, file_extension = os.path.splitext(file)
            if os.path.exists(pathname) and isPhotoFile(file_extension):
                if file_extension == '.jpg' or file_extension == '.jpeg':
                    img = PIL.Image.open(pathname)
                    exif_data = img._getexif()
                    dateTimeStr = exif_data.get(EXIF_DATETIME_TAG)
                    dt: datetime = datetime.strptime(dateTimeStr, DATETIME_PATTERN)
                    year = dt.year
                    month = dt.month
                if file_extension == '.png':
                    print('PNG format not supported yet!')
                    year = 2018
                    month = 7

                # Move/copy the file
                newpathname = dest_dir + '/' + str(year) + '/' + str(month) + '/' + file;
                print('Copies from: ', pathname, ' ==> to : ', newpathname)
                shutil.copyfile(pathname, newpathname)



if __name__ == '__main__':
    curr_dir, new_dir = initial()
    traversDirectories(curr_dir, new_dir)
else:
    print('This module can only be executed standalone')
