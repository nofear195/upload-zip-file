"""
upload
"""
import os
from zipfile import ZipFile
import zipfile
import services.base

chunk_save_folder_name = 'chunk_temp'
temp_zip_file_name = 'collation.zip'

def save_chunk_data(storage_folder_path, chunk_index, chunk_data):
    """ save chunk data to storage folder"""

    chunk_save_folder_path = f'{storage_folder_path}/{chunk_save_folder_name}'
    try:
        os.makedirs(chunk_save_folder_path)
    except FileExistsError as error:
        print('storage folder exists', error)

    try:
        chunk_save_path = f'{chunk_save_folder_path}/{chunk_index}.chunk'
        with open(chunk_save_path, 'ab') as file:
            file.write(chunk_data.read())
    except OSError as error:
        print('os error', error)
        return False
    return True


def rebuild_file(chunks_src_path, storage_folder_path, target_file_name):
    """ rebuild_file"""
    target_file_path = f'{storage_folder_path}/{target_file_name}'

    try:
        target_file = open(target_file_path, 'wb')
        chunks = os.listdir(chunks_src_path)

        for chunk in range(len(chunks)):
            path = f'{chunks_src_path}/{chunk}.chunk'
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
    return [True, 'rebuild file success']


def unzip_file(src_file_path, target_path):
    """ unzip_file"""
    with ZipFile(src_file_path, 'r') as z_f:
        try:
            for item in z_f.namelist():
                z_f.extract(item, path=target_path)
        except zipfile.BadZipfile as error:
            print('error', error)
            return [False, error]
    return [True, 'unzip success']


def process_upload(storage_folder_path):
    """ process upload"""

    # merge all chunk data
    rebuild_src_file_path = f'{storage_folder_path}/{chunk_save_folder_name}/'
    result = rebuild_file(rebuild_src_file_path,
                          storage_folder_path, temp_zip_file_name)
    print('result', result[1])

    # unzip file
    unzip_file_path = f'{storage_folder_path}/{temp_zip_file_name}'
    result = unzip_file(unzip_file_path, storage_folder_path)
    print('result', result[1])

    services.base.PROCESSING = True
