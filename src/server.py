import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v2
#from src.channel import channel_details_v2, channel_invite_v2
#from src.channel import channel_addowner_v2,channel_removeowner_v2
from src.channel import channel_join_v2 #, channel_leave_v2
from src.channels import channels_create_v2
#from src.users import users_all_v1
from src.other import clear_v2
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_share_v1
from src.channels import channels_list_v2, channels_listall_v2
from src.dm import dm_create_v1
from src.message_senddm_v2 import message_senddm_v2

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
    data = request.get_json()
    token = data['token']
    return dumps(channels_list_v2(token))

# channels/listall/v2
@APP.route('/channels/listall/v2', methods=['GET'])
def channels_listall():
    """Function that lists all channels"""
    data = request.get_json()
    token = data['token']
    return dumps(channels_listall_v2(token))

# message/send/v1
@APP.route('/message/send/v1', methods=['POST'])
def send_message():
    ''' Function that sends message to channel '''
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    return dumps(message_send_v1(token, channel_id, message))

# message/edit/v1
@APP.route('/message/edit/v1', methods=['PUT'])
def edit_message():
    ''' Function that edits a message '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    message = data['message']
    return dumps(message_edit_v1(token, message_id, message))

# message/remove/v1
@APP.route('/message/remove/v1', methods=['DELETE'])
def remove_message():
    ''' Function that removes message '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    return dumps(message_remove_v1(token, message_id))

# message/share/v1
@APP.route('/message/share/v1', methods=['POST'])
def share_message():
    ''' Function that shares message to channel or DM '''
    data = request.get_json()
    token = data['token']
    og_message_id = data['og_message_id']
    message = data['message']
    channel_id = data['channel_id']
    dm_id = data['dm_id']
    return dumps(message_share_v1(token, og_message_id, message, channel_id, dm_id))

# dm create
@APP.route('/dm/create/v1', methods = ['POST'])
def dm_create():
    data = request.get_json()
    token = data['token']
    u_ids = data['u_ids']
    return dumps(dm_create_v1(token, u_ids))

#message senddm
@APP.route('/message/senddm/v2', methods=['POST'])
def route_message_senddm_v2():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    message = data['message']
    
    return dumps(message_senddm_v2(token, dm_id, message))


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port 
