import os
from zipfile import ZipFile
import zipfile
import services.base


def unzip_file(src_file, target_path):
    """ unzip_file"""
    with ZipFile(src_file, 'r') as zf:
        try:
            for item in zf.namelist():
                zf.extract(item, path=target_path)
        except zipfile.BadZipfile as error:
            print('error', error)
            return [False, error]
    return [True, 'unZip success']


def rebuild_file(src_folder_path, target_path, target_file_name):
    """ rebuild_file"""
    target_file_path = f'{target_path}/{target_file_name}'

    try:
        target_file = open(target_file_path, 'wb')
        chunks = os.listdir(src_folder_path)

        for chunk in range(len(chunks)):
            path = f'{src_folder_path}/{chunk}.upload'
            fileobj = open(path, 'rb')
            while True:
                filebytes = fileobj.read(os.path.getsize(path))
                if not filebytes:
                    break
                target_file.write(filebytes)
            fileobj.close()
        target_file.close()
    except OSError as error:
        print('error', error)
        return [False, error]
    return [True, 'success']


def process_upload():
    """ process upload"""

    # merge all chunk data
    result = rebuild_file('./upload/test/', './upload', 'collation.zip')
    print('result', result[1])

    # unzip file
    result = unzip_file('./upload/collation.zip', './upload')
    print('result', result[1])

    services.base.PROCESSING = True
