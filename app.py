"""
Main flask server
"""

import os
from flask import render_template, request, send_from_directory, url_for
from flask_cors import CORS
# from waitress import serve
from services.base import response, CustomFlask, variable_init
import services.base
from services.upload import process_upload, save_chunk_data
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime


app = CustomFlask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["upload"] = './static/upload'

CORS(app)

variable_init()
UPLOAD_STORAGE = './static/upload'

# db information
host = os.environ.get("MYSQL_URL")
database = os.environ.get("MYSQL_DB")
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
table_name = 'uploads'

def datetime_to_string(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


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
        result = process_upload(UPLOAD_STORAGE, zip_file_name)
        if result[0] is False:
            return response(0, result[1], {'processing': False})

    return response(0, 'process upload file success', {'processing': True})


@app.route('/upload-images', methods=['POST'])
def upload_images():
    """ deal with upload"""
    data = request.get_json()
    folder_name = data['zipFileName'].replace('.zip', '')
    folder_path = f'{app.config["upload"]}/{folder_name}'
    images = os.listdir(folder_path)
    images_content = []
    for image in images:
        tmp = {'name': image, 'url': f'{folder_path}/{image}'}
        images_content.append(tmp)
    return response(0, 'success', {'image_content': images_content})


@app.route('/save-to-database', methods=['POST'])
def db():
    data = request.get_json()
    folder_name = data['zipFileName'].replace('.zip', '')
    folder_path = f'{app.config["upload"]}/{folder_name}'
    images = os.listdir(folder_path)

    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password)

        connection.autocommit = False

        if connection.is_connected():
            sql = "INSERT INTO uploads (image_name, image_url) VALUES (%s, %s);"
            for image in images:
                new_data = (image, f'{folder_path}/{image}')
                cursor = connection.cursor()
                cursor.execute(sql, new_data)
                connection.commit()
    except Error as e:
        connection.rollback()
        return response(0, e, {'save': False})

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

    return response(0, 'save to database success', {'save': True})


@app.route('/get-db-info',methods=['GET'])
def db_info():
    json_data = []
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password)

        connection.autocommit = False

        if connection.is_connected():
            sql = f"SELECT * FROM {table_name};"
            cursor = connection.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()

            # Convert datetime objects to strings
            for row in data:
                json_row = {}
                for i, column in enumerate(cursor.description):
                    if isinstance(row[i], datetime):
                        json_row[column[0]] = datetime_to_string(row[i])
                    else:
                        json_row[column[0]] = row[i]
                json_data.append(json_row)

    except Error as e:
        connection.rollback()
        return response(0, e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    
    return response(0, 'get all data from table', {'db_data': json_data})


# def main():
#     """ run flask server"""
#     # for develop mode
#     app.run(host='0.0.0.0', port=5000, debug=True)
#     # for production mode
#     # serve(app,host="0.0.0.0",port=8080)


# if __name__ == "__main__":
#     main()
