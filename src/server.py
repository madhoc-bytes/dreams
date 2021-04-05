import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v2
from src.channel import channel_details_v2, channel_join_v2, channel_invite_v2
from src.channels import channels_create_v2
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
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return_value = auth_register_v2(email, password, name_first, name_last)
    return dumps(return_value)

# channel join
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    return dumps(channel_join_v2(token, channel_id))

# channel invite
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return dumps(channel_invite_v2(token, channel_id, u_id))

# channel details
@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(channel_details_v2(token, channel_id))

# channel create
@APP.route('/channels/create', methods = ['POST'])
def server_channels_create():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    return_value = channels_create_v2(token, name, is_public)
    return dumps(return_value)

# clear 
@APP.route('/clear/v2', methods = ['DELETE'])
def clear():
    return dumps(clear_v2)

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port 

