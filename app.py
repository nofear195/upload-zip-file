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
import mysql.connector
from mysql.connector import Error


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

@app.route('/db', methods=['GET'])
def db():
    try:
        # 連接 MySQL/MariaDB 資料庫
        host = os.environ.get("MYSQL_URL")
        database = os.environ.get("MYSQL_DB")
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")

        connection = mysql.connector.connect(
            host=host,# 主機名稱
            database=database, # 資料庫名稱
            user=user,        # 帳號
            password=password)  # 密碼

        if connection.is_connected():

            # 顯示資料庫版本
            db_Info = connection.get_server_info()
            print("資料庫版本：", db_Info)

            # 顯示目前使用的資料庫
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("目前使用的資料庫：", record)

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

    return response(0, 'success', {'processing': True})

# def main():
#     """ run flask server"""
#     # for develop mode
#     app.run(host='0.0.0.0', port=5000, debug=True)
#     # for production mode
#     # serve(app,host="0.0.0.0",port=8080)


# if __name__ == "__main__":
#     main()
