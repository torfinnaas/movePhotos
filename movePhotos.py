#!/usr/bin/env python3
import os
import sys
import shutil
from datetime import datetime
import PIL.Image
import PIL.ExifTags





VERSION='0.0.1'
EXIF_DATETIME_TAG=36867
# Date/time format in EXIF data from jpeg files: '2016:03:25 21:29:36'
DATETIME_PATTERN='%Y:%m:%d %H:%M:%S'
monthDirName = ['01 Januar', '02 Februar', '03 Mars', '04 April', '05 Mai', '06 Juni',
                '07 Juli', '08 August', '09 September', '10 Oktober', '11 November', '12 Desember']
filesMoved = 0
maxNoFiles = -1  # No limit




def isPhotoFile(fileExtension):
    photoExtensions = [".jpg", ".jpeg"]
    if fileExtension in photoExtensions:
        return True
    else:
        return False


def initial():
    global maxNoFiles

    print('Welcome to MovePhotos version', VERSION)

    src_dir = os.path.dirname(os.path.realpath(__file__))

    if len(sys.argv) < 2:
        print(f'Usage: {os.path.basename(__file__)} <destiantion directory>')
        sys.exit(0)
    else:
        if len(sys.argv) >= 3:
            maxNoFiles = int(sys.argv[2])
        else:
            maxNoFiles = -1
        dest_dir = str(sys.argv[1])
        print('Moving {} files from {} to {}'.format(maxNoFiles, src_dir, dest_dir))

    return src_dir, dest_dir




def traversDirectories(src_dir: object, dest_dir: object) -> object:
    global filesMoved
    global maxNoFiles

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
                # if file_extension == '.png':
                #    print('PNG format not supported yet!')

                # Move/copy the file
                newPathName = dest_dir + '/' + str(year) + '/' + monthDirName[month-1] + '/' + file;
                print('Moving from: ', pathname, ' ==> to : ', newPathName)
                #shutil.copy2(pathname, newPathName)
                try:
                    shutil.move(pathname, newPathName)
                    filesMoved += 1
                    if maxNoFiles != -1:
                        if filesMoved >= maxNoFiles:
                            break
                except:
                    print(f'*** file could not be moved ({newPathName})')

        if maxNoFiles != -1:
            if filesMoved >= maxNoFiles:
                print('- max files moved!')
                break



if __name__ == '__main__':
    curr_dir, new_dir = initial()
    traversDirectories(curr_dir, new_dir)
    print(f'Total files moved: {filesMoved}')
else:
    print('This module can only be executed standalone')
