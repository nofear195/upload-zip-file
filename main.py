"""
Main flask server
"""
import os
from flask import Flask, render_template, request
from flask_cors import CORS
# from waitress import serve
from services.base import response,CustomFlask,variable_init
import services.base
from services.upload import process_upload


app = CustomFlask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

variable_init()


@app.route('/')
def home():
    """ home template"""
    return render_template('home.html')


@app.route('/chunk-data-store', methods=['POST'])
def store_chunk_data():
    """ store chunk data"""
    chunk_data = request.files['chunkData']
    chunk_index = request.form.get('chunkIndex')

    services.base.PROCESSING = False

    try:
        os.makedirs('./upload/test')
    except FileExistsError:
        print('file exit')

    try:
        save_path = f'./upload/test/{chunk_index}.upload'
        with open(save_path, 'ab') as file:
            file.write(chunk_data.read())
    except OSError as error:
        print('error save', error)
    return response(0, 'success')


@app.route('/deal-with-upload', methods=['POST'])
def deal_with_upload():
    """ deal with upload"""

    if services.base.PROCESSING is False:
        process_upload()
        return response(0, 'success',{'processing':False})

    return response(0, 'success',{'processing':True})


def main():
    """ run flask server"""
    # for develop mode
    app.run(host='0.0.0.0', port=8080, debug=True)
    # for production mode
    # serve(app,host="0.0.0.0",port=8080)


if __name__ == "__main__":
    main()
