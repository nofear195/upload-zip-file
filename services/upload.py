"""
upload function
"""

import os
from zipfile import ZipFile
import zipfile
from shutil import rmtree, move
from uuid import uuid4, UUID
import services.base  # pylint: disable=import-error


def is_valid_uuid_str(value):
    """ check input string is valid uuid"""
    try:
        UUID(value)
        return True
    except ValueError:
        return False


# def transfer_encode_error(file):
#     """ deal with encode error"""

#     if file.lower().endswith(('.png', '.jpg', '.jpeg')):
#         # print("file",file)
#         #  中文亂碼編碼 、過濾特殊字元
#         right_name = file.encode('cp437').decode(
#             'big5', 'ignore').replace("'", "")
#         split_name = file.split('/')
#         return f'{split_name[0]}/{right_name}.eee'
#     return file


def save_chunk_data(storage_folder_path, zip_file_name, chunk_index, chunk_data):
    """ save chunk data to storage folder"""

    # check if zip file exist and delete it
    zip_file_path = f'{storage_folder_path}/{zip_file_name}.zip'
    if os.path.exists(zip_file_path):
        print('upload zip exist')
        os.remove(zip_file_path)

    if services.base.UPLOAD_UUID == '':
        services.base.UPLOAD_UUID = str(uuid4())

    temp_folder_name = f'{zip_file_name}_{services.base.UPLOAD_UUID}'

    # delete all fail upload folder
    folder_name_list = os.listdir(storage_folder_path)
    for folder_name in folder_name_list:
        split_folder_name = folder_name.split("_")
        vaild_str_input = str(uuid4()) if len(
            split_folder_name) == 1 else split_folder_name[1]
        if folder_name != temp_folder_name and is_valid_uuid_str(vaild_str_input):
            try:
                rmtree(f'{storage_folder_path}/{folder_name}')
            except OSError as error:
                print('os error ', error)

    chunk_save_folder_path = f'{storage_folder_path}/{temp_folder_name}'

    # delete all fail upload folder
    folder_list = os.listdir(storage_folder_path)
    for folder in folder_list:
        if folder.find(services.base.UPLOAD_UUID) == -1:
            rmtree(f'{storage_folder_path}/{folder}')

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
        return [False, error]
    return [True, f'uploading chunk no.{chunk_index} success']


def rebuild_file(chunks_src_path, storage_folder_path, target_file_name):
    """ rebuild_file"""
    target_file_path = f'{storage_folder_path}/{target_file_name}.zip'

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


def unzip_file(src_file_path, storage_folder_path, zip_file_name):
    """ unzip_file"""

    temp_save_folder = f'{storage_folder_path}/unzip_{services.base.UPLOAD_UUID}'
    try:
        os.makedirs(temp_save_folder)
    except FileExistsError as error:
        print('storage folder exists', error)

    with ZipFile(src_file_path, 'r') as z_f:
        try:
            for item in z_f.namelist():
                z_f.extract(item, path=temp_save_folder)
        except zipfile.BadZipfile as error:
            print('error', error)
            return [False, error]

    subfolders = [f.path for f in os.scandir(temp_save_folder) if f.is_dir()]

    for sub in subfolders:
        for f in os.listdir(sub):
            src = os.path.join(sub, f)
            dst = os.path.join(temp_save_folder, f)
            move(src, dst)
    for sub in subfolders:
        rmtree(sub)
    os.rename(temp_save_folder, f'{storage_folder_path}/{zip_file_name}')

    return [True, 'unzip success']


def process_upload(storage_folder_path, zip_file_name):
    """ process upload"""

    # merge all chunk data
    rebuild_src_file_path = f'{storage_folder_path}/{zip_file_name}_{services.base.UPLOAD_UUID}/'
    result = rebuild_file(rebuild_src_file_path,
                          storage_folder_path, zip_file_name)
    print('result', result[1])
    if (result[0] is False):
        return [result[0], result[1]]
    # delete tmp_folder
    rmtree(rebuild_src_file_path)

    # unzip file
    unzip_file_path = f'{storage_folder_path}/{zip_file_name}.zip'

    result = unzip_file(unzip_file_path, storage_folder_path, zip_file_name)
    print('result', result[1])
    if (result[0] is False):
        return [result[0], result[1]]

    #delete zip file
    os.remove(unzip_file_path)

    # reset variable to init
    services.base.UPLOAD_UUID = ''
    services.base.PROCESSING = True
    return [True, 'process success']
