# upload zip file

Projcet basic environment and Packages

    Python : 3-alpine3.17
    Backend sever :  Flask
    Frontend framework : Vue 3 with Options API
    UI toolkit : Bootstrap 5
    http requests: Axios

## Getting Started

### Flask server settings (with virtual environment)

Create a python virtual environments (venv) 

    python -m venv venv

Activate the virtual environments

    . venv/bin/activate

Download the python package using the **requirements.txt** file

    pip install -r requirements.txt

Exit virtual environments

    deactivate

add below code on vscode setting.json which can also define in **devcontainer.json**
    
    "python.defaultInterpreterPath": "/usr/local/venv/bin/python"

	"python.linting.pylintPath": "/usr/local/venv/bin/pylint"

### Flask server settings (without virtual environment)

Download the python package using the **requirements.txt** file

    pip install -r requirements.txt

## Run server

    flask run

## Run server via docker   

    docker container run --publish 8000:5000 nofear195/upload-zip-file-web:latest

### reference link & TBD

 - [Mac zip compress without __MACOSX folder?](https://stackoverflow.com/questions/10924236/mac-zip-compress-without-macosx-folder)
 - This command works on my mac : `zip -r -X Target.zip Source -x "*.DS_Store"`

 - [Upload Image,convert it to zip( client side ) and then upload to server](https://stackoverflow.com/questions/48583915/upload-image-convert-it-to-zip-client-side-and-then-upload-to-server)
 - [js zip](https://github.com/Stuk/jszip)

 - [Flask - Uploading Files](https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/)