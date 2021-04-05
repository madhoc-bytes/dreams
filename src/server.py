import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.channels import channels_create_v2

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
#admin userpermission change
@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def route_admin_userpermission_change():

    token = request.form.get("token")
    u_id = int(request.form.get("u_id"))
    p_id = int(request.form.get("permission_id"))
    return_values = adminuserpermissionchangev1(token, u_id, p_id)

    return dumps(return_values)

#####################
#####################
#####################
@APP.route('/dm/create/v2', methods=['POST'])
def route_dm_create_v2():

    token = request.form.get("token")
    u_ids = int(request.form.get("u_ids"))
    return_values = dm_create_v2(token, u_ids)

    return dumps(return_values)

@APP.route('/dm/remove/v2', methods=['DELETE'])
def route_dm_remove_v2():

    token = request.form.get("token")
    dm_id = int(request.form.get("dm_id"))
    return_values = dm_create_v2(token, dm_id)

    return dumps(return_values)


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
