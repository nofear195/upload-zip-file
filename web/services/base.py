"""
basic setting
"""

from flask import Flask

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

PROCESSING = False
UPLOAD_UUID = ''

def variable_init():
    """ init variable"""
    global PROCESSING,UPLOAD_UUID # pylint: disable=global-statement
    PROCESSING = False
    UPLOAD_UUID = ''
