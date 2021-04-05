import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v2
from src.channel import channel_details_v2, channel_invite_v2
from src.channel import channel_addowner_v2,channel_removeowner_v2
from src.channel import channel_join_v2, channel_leave_v2
from src.channels import channels_create_v2
from src.users import users_all_v1
from src.other import clear_v2
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_share_v1
from src.channel import channel_details_v2
from src.channels import channels_list_v2, channels_listall_v2
from src.dm_invite_v1 import dm_invite_v1

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
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    return_value = auth_register_v2(email, password, name_first, name_last)
    return dumps(return_value)

# channel join
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    return dumps(channel_join_v2(token, channel_id))

# channel leave
@APP.route("/channel/leave/v2", methods=['POST'])
def channel_leave():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    return dumps(channel_leave_v2(token, channel_id))

# channel invite
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    return dumps(channel_invite_v2(token, channel_id, u_id))

# channel details
@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    return dumps(channel_details_v2(token, channel_id))

# channel addowner
@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    return dumps(channel_addowner_v2(token, channel_id, u_id))

# channel removeowner
@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    return dumps(channel_removeowner_v2(token, channel_id, u_id))

# channel create
@APP.route('/channels/create/v2', methods = ['POST'])
def server_channels_create():
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = data['is_public']
    return_value = channels_create_v2(token, name, is_public)
    return dumps(return_value)

# users all
@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    token = request.args.get('token')
    return dumps(users_all_v1(token))

# clear 
@APP.route('/clear/v1', methods = ['DELETE'])
def clear():
    return dumps(clear_v2())


# channels/list/v2
@APP.route('/channels/list/v2', methods=['GET'])
def channels_list():
    """Function that lists all channels for which a certain user has access"""

    token = request.form.get('token')
    return_value = channels_list_v2(token)
    return dumps(return_value)

# channels/listall/v2
@APP.route('/channels/listall/v2', methods=['GET'])
def channels_listall():
    """Function that lists all channels"""

    token = request.form.get('token')
    return_value = channels_listall_v1(token)
    return dumps(return_value)

# message/send/v1
@APP.route('/message/send/v1', methods=['POST'])
def send_message():
    ''' Function that sends message to channel '''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    return_value = message_send_v1(token, channel_id, message)
    return dumps(return_value)

# message/edit/v1
@APP.route('/message/edit/v1', methods=['PUT'])
def edit_message():
    ''' Function that edits a message '''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    return_value = message_edit_v1(token, channel_id, message)
    return dumps(return_value)

# message/remove/v1
@APP.route('/message/remove/v1', methods=['DELETE'])
def remove_message():
    ''' Function that removes message '''

    token = request.form.get('token')
    message_id = request.form.get('message_id')

    return_value = message_remove_v1(token, message_id)
    return dumps(return_value)

# message/share/v1
@APP.route('/message/share/v1', methods=['POST'])
def share_message():
    ''' Function that shares message to channel or DM '''

    token = request.form.get('token')
    
    og_message_id = request.form.get('og_message_id')
    message = request.form.get('message')
    channel_id = request.form.get('channel_id')
    dm_id = request.form.get('dm_id')

    return_value = message_share_v1(token, og_message_id, message, channel_id, dm_id)
    return dumps(return_value)

# dm/invite/v1
@APP.route('dm/invite/v1', methods=['POST'])
def dm_invite():
    ''' Function that invites user to DM '''
    token = request.form.get('token')
    dm_id = request.form.get('dm_id')
    u_id = request.form.get('u_id')

    return_value = dm_invite_v1(token, dm_id, u_id)
    return dumps(return_value)

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return json.dumps(channel_details_v2(token, channel_id))


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
