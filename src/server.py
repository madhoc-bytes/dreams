import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v2
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1
from src.other import clear_v2

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

# auth register
@APP.route('/auth/register/v2', methods=['POST'])
def auth_register():
    global email, password, name_first, name_last
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    info = auth_register_v2(email, password, name_first, name_last)
    return dumps(info)

@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():
    
    response = request.get_json()
    email = response['email']
    password = response['password']
    info = auth_login_v2(email, password)
    return dumps(info)

@APP.route('/auth/logout/v2', methods=['POST'])
def auth_logout():

    token = request.form.get('token')
    return_value = auth_logout_v2(token)
    return dumps(return_value)

@APP.route('/user/profile/v1', methods=['GET'])
def user_profile():

    token = request.args.get('token')
    auth_user_id = request.args.get('u_id')
    return_value = user_profile_v1(token, auth_user_id)
    return dumps(return_value)

@APP.route('/user/profile/setname/v1', methods=['PUT'])
def user_profile_setname():

    token = request.get_json()['token']
    name_first = request.get_json()['name_first']
    name_last = request.get_json()['name_last']
   
    return_value = user_profile_setname_v1(token, name_first, name_last)
    return dumps(return_value)


@APP.route('/user/profile/setemail/v1', methods=['PUT'])
def user_profile_setemail():

    token = request.get_json()['token']
    email = request.get_json()['email']
    return_value = user_profile_setemail_v1(token, email)
    return dumps(return_value)


@APP.route('/user/profile/sethandle/v1', methods=['PUT'])
def user_profile_sethandle():

    token = request.get_json()['token']
    handle_str = request.get_json()['handle_str']
    return_value = user_profile_sethandle_v1(token, handle_str)
    return dumps(return_value)



##########################################################################################################################################
# clear 
@APP.route('/clear/v1', methods = ['DELETE'])
def clear():
    return dumps(clear_v2())

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port 
