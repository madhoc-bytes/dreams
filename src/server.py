import sys
from src import config
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src.data import messages
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_share_v1
from src.channel import channel_details_v2
from src.channels import channels_list_v2, channels_listall_v2

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
def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# channels/list/v2
@APP.route('/channels/list/v2', methods=['GET'])
def channels_list():
    """Function that lists all channels for which a certain user has access"""

    token = request.form.get('token')
    auth_user_id = get_user_from_token(token)
    return_value = channels_list_v2(auth_user_id)
    return dumps(return_value)

# channels/listall/v2
@APP.route('/channels/listall/v2', methods=['GET'])
def channels_listall():
    """Function that lists all channels"""

    token = request.form.get('token')
    auth_user_id = get_user_from_token(token)
    return_value = channels_listall_v1(auth_user_id)
    return dumps(return_value)

# message/send/v1
@APP.route('/message/send/v1', methods=['POST'])
def send_message():
    ''' Function that sends message to channel '''

    token = request.form.get('token')
    auth_user_id = get_user_from_token(token)
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    return_value = message_send_v1(auth_user_id, channel_id, message)
    return dumps(return_value)

# message/edit/v1
@APP.route('/message/edit/v1', methods=['PUT'])
def edit_message():
    ''' Function that edits a message '''

    token = request.form.get('token')
    auth_user_id = get_user_from_token(token)
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    return_value = message_edit_v1(auth_user_id, channel_id, message)
    return dumps(return_value)

# message/remove/v1
@APP.route('/message/remove/v1', methods=['DELETE'])
def remove_message():
    ''' Function that removes message '''

    token = request.form.get('token')
    auth_user_id = get_user_from_token(token)
    message_id = request.form.get('message_id')

    return_value = message_remove_v1(auth_user_id, message_id)
    return dumps(return_value)

# message/share/v1
@APP.route('/message/share/v1', methods=['POST'])
def share_message():
    ''' Function that shares message to channel or DM '''

    token = request.form.get('token')
    auth_user_id = get_user_from_token(token)
    
    og_message_id = request.form.get('og_message_id')
    message = request.form.get('message')
    channel_id = request.form.get('channel_id')
    dm_id = request.form.get('dm_id')

    return_value = message_share_v1(auth_user_id, og_message_id, message, channel_id, dm_id)
    return dumps(return_value)

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return json.dumps(channel_details_v2(token, channel_id))


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
