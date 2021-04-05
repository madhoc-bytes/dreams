import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import config

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port

@APP.route('/auth/register/v2', methods=['POST'])
def auth_register():

    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return_value = auth_register_v2(email, password, name_first, name_last)
    return dumps(return_value)

@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():

    email = request.form.get('email')
    password = request.form.get('password')

    return_value = auth_login_v2(email, password)
    return dumps(return_value)

@APP.route('/auth/logout/v2', methods=['POST'])
def auth_logout():

    token = request.form.get('token')
    return_value = auth_logout_v2(token)
    return dumps(return_value)