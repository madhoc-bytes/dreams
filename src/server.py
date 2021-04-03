import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.channels import channels_create_v2
from src.other import adminuserpermissionchangev1

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

#####################
#####################
#####################
#channels 
@APP.route('/channels/create', methods = ['POST'])
def server_channels_create():

    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    return_value = channels_create_v2(token, name, is_public)
    return dumps(return_value)
#####################
#####################
#####################
#admin_userpermission_change


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
