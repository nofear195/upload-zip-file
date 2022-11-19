# in devcontainer.json put below code
# "postCreateCommand": "sh ./postCreateCommand.sh",

python -m venv venv
. venv/bin/activate
pip install -r requirements.txt