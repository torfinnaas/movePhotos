#!/usr/bin/env python3
import os
import sys
import shutil
from datetime import datetime
from PIL import Image
import argparse




VERSION='0.0.1'
EXIF_DATETIME_TAG=36867
# Date/time format in EXIF data from jpeg files: '2016:03:25 21:29:36'
DATETIME_PATTERN='%Y:%m:%d %H:%M:%S'
monthDirName = ['01 Januar', '02 Februar', '03 Mars', '04 April', '05 Mai', '06 Juni',
                '07 Juli', '08 August', '09 September', '10 Oktober', '11 November', '12 Desember']
filesMoved = 0
maxNoFiles = -1  # No limit
operation = 'Moving'  # moving or copy




def isPhotoFile(fileExtension):
    photoExtensions = [".jpg", ".jpeg", ".png"]
    if fileExtension in photoExtensions:
        return True
    else:
        return False


def initial():
    global maxNoFiles, operation

    print('MovePhotos version', VERSION)

    parser = argparse.ArgumentParser()
    parser.add_argument('destDirectory', default=None, help='Destination directory to move or copy the files to')
    parser.add_argument("--maxCount", help="the maximum number of files to move", default=-1)
    parser.add_argument("--copy", help="copies files instead of moving them", action="store_true")
    args = parser.parse_args()

    src_dir = os.path.dirname(os.path.realpath(__file__))
    dest_dir = args.destDirectory
    maxNoFiles = -1 if args.maxCount == '-1' else int(args.maxCount)
    operation = 'Copying' if args.copy else 'Moving'

    if maxNoFiles != -1:
        print('{} {} files from {} to {}'.format(operation, maxNoFiles, src_dir, dest_dir))
    else:
        print('{} files from {} to {}'.format(operation, src_dir, dest_dir))

    return src_dir, dest_dir









def traversDirectories(src_dir: object, dest_dir: object) -> object:
    global filesMoved, maxNoFiles, operation

    for root, dirs, files in os.walk(src_dir):
        print(f'Directory: {root}:')

        for file in files:
            pathname = os.path.join(root, file)
            temp, file_extension = os.path.splitext(file)
            if os.path.exists(pathname) and isPhotoFile(file_extension):
                if file_extension == '.jpg' or file_extension == '.jpeg':
                    img = Image.open(pathname)
                    exif_data = img._getexif()
                    dateTimeStr = exif_data.get(EXIF_DATETIME_TAG)
                    dt: datetime = datetime.strptime(dateTimeStr, DATETIME_PATTERN)
                    year = dt.year
                    month = dt.month

                if file_extension == '.png':
                    print(f'*** PNG format not supported yet! ({pathname})')
                    continue

                # Move/copy the file
                newPathName = dest_dir + '/' + str(year) + '/' + monthDirName[month-1] + '/' + file;

                for i in range(2):   # retry one time in case of missing directory
                    try:
                        if operation == 'Moving':
                            shutil.move(pathname, newPathName)
                        else:
                            shutil.copy2(pathname, newPathName)

                        print(f'  {operation} from: {pathname} ==> to : {newPathName}')
                        filesMoved += 1
                        break    # don't retry
                    except FileNotFoundError:
                        # probably the directory does not exists.Try to create
                        if not os.path.exists(dest_dir + '/' + str(year)):
                            os.mkdir(dest_dir + '/' + str(year))
                        if not os.path.exists(dest_dir + '/' + str(year) + '/' + monthDirName[month-1]):
                            os.mkdir(dest_dir + '/' + str(year) + '/' + monthDirName[month-1])
                        continue   # retry the copy/move
                    except:
                        print(f'Unknown exception: {sys.exc_info()[1]}')
                        print(f'*** file could not be handled ({newPathName})')
                        break

            if maxNoFiles != -1:
                if filesMoved >= maxNoFiles:
                    break


        if maxNoFiles != -1:
            if filesMoved >= maxNoFiles:
                print('- max files handled!')
                break


def main():
    curr_dir, new_dir = initial()
    traversDirectories(curr_dir, new_dir)
    print(f'Total files handled: {filesMoved}')





if __name__ == '__main__':
    main()
else:
    print('This program can only be executed standalone, not as a module!')
