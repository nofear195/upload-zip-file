"""
Main flask server
"""

import os
from flask import render_template, request
from flask_cors import CORS
# from waitress import serve
from services.base import response, CustomFlask, variable_init
import services.base
from services.upload import process_upload, save_chunk_data


app = CustomFlask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

variable_init()
UPLOAD_STORAGE = './upload'


@app.route('/')
def home():
    """ home template"""
    return render_template('home.html')


@app.route('/chunk-data-store', methods=['POST'])
def store_chunk_data():
    """ store chunk data"""
    chunk_data = request.files['chunkData']
    chunk_index = request.form.get('chunkIndex')
    zip_file_name = request.form.get('zipFileName')

    zip_file_name = zip_file_name.replace('.zip', '')

    services.base.PROCESSING = False

    try:
        os.makedirs(UPLOAD_STORAGE)
    except FileExistsError:
        pass

    result = save_chunk_data(
        UPLOAD_STORAGE, zip_file_name, chunk_index, chunk_data)
    if result[0] is False:
        return response(1, result[1], {'save': result[0]})

    return response(0, result[1], {'save': result[0]})


@app.route('/deal-with-upload', methods=['POST'])
def deal_with_upload():
    """ deal with upload"""

    data = request.get_json()
    zip_file_name = data['zipFileName']
    zip_file_name = zip_file_name.replace('.zip', '')

    if services.base.PROCESSING is False:
        process_upload(UPLOAD_STORAGE, zip_file_name)
        return response(0, 'success', {'processing': False})

    return response(0, 'success', {'processing': True})


# def main():
#     """ run flask server"""
#     # for develop mode
#     app.run(host='0.0.0.0', port=80, debug=True)
#     # for production mode
#     # serve(app,host="0.0.0.0",port=8080)


# if __name__ == "__main__":
#     main()
