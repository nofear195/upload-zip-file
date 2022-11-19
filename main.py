"""
Main flask server
"""
import os
import shutil
from zipfile import ZipFile
import zipfile
from flask import Flask, render_template, request
from flask_cors import CORS
# from waitress import serve


def response(code, message, data=None):
    """ for unify response"""
    # code=0 for success, code=1 for fail
    return {'code': code, 'message': message, 'data': data}


class CustomFlask(Flask):
    """ custom flask setting"""
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        # I changed the jinja expression delimiter from {{...}} to %%...%%
        # because it conflicts with the Vue template syntax {{}}
        variable_start_string='%%',
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)


PROCESSING = False


def process_upload():
    """ process upload"""

    global PROCESSING
    PROCESSING = True
    # merge all chunk data
    result = rebuild_file('./upload/test/', './upload', 'collation.zip')
    print('result', result[1])

    # unzip file
    result = unzip_file('./upload/collation.zip', './upload')
    print('result', result[1])


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


@app.route('/')
def home():
    """ home template"""
    return render_template('home.html')


@app.route('/chunk-data-store', methods=['POST'])
def store_chunk_data():
    """ store chunk data"""
    chunk_data = request.files['chunkData']
    chunk_index = request.form.get('chunkIndex')

    try:
        os.makedirs('./upload/test')
    except FileExistsError:
        print('file exit')

    try:
        save_path = f'./upload/test/{chunk_index}.upload'
        with open(save_path, 'ab') as file:
            file.write(chunk_data.read())
    except OSError as error:
        print('error save',error)
    return response(0, 'success')


@app.route('/deal-with-upload', methods=['POST'])
def deal_with_upload():
    """ deal with upload"""

    if PROCESSING is False:
        process_upload()
        return response(0, 'start')   
    return response(0, 'end')


def main():
    """ run flask server"""
    # for develop mode
    app.run(host='0.0.0.0', port=8080, debug=True)
    # for production mode
    # serve(app,host="0.0.0.0",port=8080)


if __name__ == "__main__":
    main()
