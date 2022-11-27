"""
Main flask server
"""
from flask import render_template, request
from flask_cors import CORS
# from waitress import serve
from services.base import response, CustomFlask, variable_init
import services.base
from services.upload import process_upload, save_chunk_data
from uuid import uuid4

app = CustomFlask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

variable_init()
storage_folder = './upload'


@app.route('/')
def home():
    """ home template"""
    return render_template('home.html')


@app.route('/chunk-data-store', methods=['POST'])
def store_chunk_data():
    """ store chunk data"""
    chunk_data = request.files['chunkData']
    chunk_index = request.form.get('chunkIndex')

    if services.base.UPLOAD_UUID == '':
        services.base.UPLOAD_UUID = str(uuid4())
    print('uuid',services.base.UPLOAD_UUID)
    services.base.PROCESSING = False

    result = save_chunk_data(storage_folder, chunk_index, chunk_data)
    if result is False:
        return response(1, 'fail')

    return response(0, 'success')


@app.route('/deal-with-upload', methods=['POST'])
def deal_with_upload():
    """ deal with upload"""

    if services.base.PROCESSING is False:
        process_upload(storage_folder)
        return response(0, 'success', {'processing': False})

    return response(0, 'success', {'processing': True})


def main():
    """ run flask server"""
    # for develop mode
    app.run(host='0.0.0.0', port=8080, debug=True)
    # for production mode
    # serve(app,host="0.0.0.0",port=8080)


if __name__ == "__main__":
    main()
