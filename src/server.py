import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.data import persist_data
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v2
from src.dm import dm_create_v1, dm_details_v1, dm_invite_v1, dm_leave_v1, dm_list_v1, dm_messages_v1, dm_remove_v1
from src.channel import channel_details_v2, channel_invite_v2
from src.channel import channel_addowner_v2,channel_removeowner_v2, channel_messages_v2
from src.channel import channel_join_v2, channel_leave_v2
from src.channels import channels_create_v2
from src.standup import standup_active_v1, standup_start_v1, standup_send_v1
from src.message import message_send_v2, message_edit_v1, message_remove_v1, message_share_v1, message_pin_v1, message_unpin_v1
from src.message import message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_unreact_v1
from src.channels import channels_list_v2, channels_listall_v2
from src.users import users_all_v1, users_stats_v1
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1, user_stats_v1
from src.message_senddm_v2 import message_senddm_v2
from src.admin_userpermission_change_v1 import adminuserpermissionchangev1
from src.search import search_v2
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
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    return_value = auth_register_v2(email, password, name_first, name_last)
    persist_data()
    return dumps(return_value)

@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    return_value = auth_login_v2(email, password)
    persist_data()
    return dumps(return_value)

@APP.route('/auth/logout/v2', methods=['POST'])
def auth_logout():
    data = request.get_json()
    token = data['token']
    return_value = auth_logout_v2(token)
    persist_data()
    return dumps(return_value)

# user stats
@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
    token = request.args.get('token')
    return dumps(user_stats_v1(token))

@APP.route('/user/profile/v1', methods=['GET'])
def user_profile():
    token = request.args.get('token')
    auth_user_id = int(request.args.get('u_id'))
    return_value = user_profile_v1(token, auth_user_id)
    return dumps(return_value)

@APP.route('/user/profile/setname/v1', methods=['PUT'])
def user_profile_setname():
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    return_value = user_profile_setname_v1(token, name_first, name_last)
    persist_data()
    return dumps(return_value)


@APP.route('/user/profile/setemail/v1', methods=['PUT'])
def user_profile_setemail():
    data = request.get_json()
    token = data['token']
    email = data['email']
    return_value = user_profile_setemail_v1(token, email)
    persist_data()
    return dumps(return_value)


@APP.route('/user/profile/sethandle/v1', methods=['PUT'])
def user_profile_sethandle():
    data = request.get_json()
    token = data['token']
    handle_str = data['handle_str']
    return_value = user_profile_sethandle_v1(token, handle_str)
    persist_data()
    return dumps(return_value)


# channel join
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    persist_data()
    return dumps(channel_join_v2(token, channel_id))

# channel messages
@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return dumps(channel_messages_v2(token, channel_id, start))

# channel leave
@APP.route("/channel/leave/v2", methods=['POST'])
def channel_leave():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    persist_data()
    return dumps(channel_leave_v2(token, channel_id))

# channel invite
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    persist_data()
    return dumps(channel_invite_v2(token, channel_id, u_id))

# channel details
@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(channel_details_v2(token, channel_id))

# channel addowner
@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    persist_data()
    return dumps(channel_addowner_v2(token, channel_id, u_id))

# channel removeowner
@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    persist_data()
    return dumps(channel_removeowner_v2(token, channel_id, u_id))

# channel create
@APP.route('/channels/create/v2', methods = ['POST'])
def server_channels_create():
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = data['is_public']
    return_value = channels_create_v2(token, name, is_public)
    persist_data()
    return dumps(return_value)

#admin userpermission change
@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def admin_userpermission_change():
    data = request.get_json()
    token = data['token']    
    u_id = data['u_id']
    p_id = data['permission_id']
    persist_data()
    return dumps(adminuserpermissionchangev1(token, u_id, p_id))


# channels/list/v2
@APP.route('/channels/list/v2', methods=['GET'])
def channels_list():
    """Function that lists all channels for which a certain user has access"""
    token = request.args.get('token')
    return dumps(channels_list_v2(token))

# channels/listall/v2
@APP.route('/channels/listall/v2', methods=['GET'])
def channels_listall():
    """Function that lists all channels"""
    token = request.args.get('token')
    return dumps(channels_listall_v2(token))

# message/send/v1
@APP.route('/message/send/v1', methods=['POST'])
def send_message():
    ''' Function that sends message to channel '''
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    persist_data()
    return dumps(message_send_v2(token, channel_id, message))

# message/edit/v1
@APP.route('/message/edit/v1', methods=['PUT'])
def edit_message():
    ''' Function that edits a message '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    message = data['message']
    persist_data()
    return dumps(message_edit_v1(token, message_id, message))

# message/remove/v1
@APP.route('/message/remove/v1', methods=['DELETE'])
def remove_message():
    ''' Function that removes message '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    persist_data()
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
    persist_data()
    return dumps(message_share_v1(token, og_message_id, message, channel_id, dm_id))

# message/pin/v1
@APP.route('/message/pin/v1', methods=['POST'])
def pin_message():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    return dumps(message_pin_v1(token, message_id))

# message/unpin/v1
@APP.route('/message/unpin/v1', methods=['POST'])
def unpin_message():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    return dumps(message_unpin_v1(token, message_id))

#message
@APP.route('/message/senddm/v2', methods=['POST'])
def message_senddm():
    data = request.get_json()
    token = data['token']    
    dm_id = data['dm_id']
    message =data['message']
    persist_data()
    return dumps(message_senddm_v2(token, dm_id, message))

# users all
@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    token = request.args.get('token')
    return dumps(users_all_v1(token))

# users stats
@APP.route("/users/stats/v1", methods=['GET'])
def users_stats():
    token = request.args.get('token')
    return dumps(users_stats_v1(token))

# search
@APP.route("/search/v2", methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = token = request.args.get('query_str')
    return dumps(search_v2(token, query_str))

# clear 
@APP.route('/clear/v1', methods = ['DELETE'])
def clear():
    persist_data()
    return dumps(clear_v2())

#standup start
@APP.route('/standup/start/v1', methods = ['POST'])
def standup_start():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    length = data['length']
    persist_data()
    return dumps(standup_start_v1(token, channel_id, length))
#standup_active
@APP.route('/standup/active/v1', methods = ['GET'])
def is_active():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(standup_active_v1(token, channel_id))
#standup_send
@APP.route('/standup/send/v1', methods = ['POST'])
def standup_send():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    persist_data()
    return dumps(standup_send_v1(token, channel_id, message))

# dm create
@APP.route('/dm/create/v1', methods = ['POST'])
def dm_create():
    data = request.get_json()
    token = data['token']
    u_ids = data['u_ids']
    persist_data()
    return dumps(dm_create_v1(token, u_ids))

# dm details
@APP.route('/dm/details/v1', methods = ['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    return dumps(dm_details_v1(token, dm_id))

# dm list
@APP.route('/dm/list/v1', methods = ['GET'])
def dm_list():
    token = request.args.get('token')
    return dumps(dm_list_v1(token))

# dm invite
@APP.route('/dm/invite/v1', methods = ['POST'])
def dm_invite():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    u_id = data['u_id']
    persist_data()
    return dumps(dm_invite_v1(token, dm_id, u_id))

# dm messages
@APP.route('/dm/messages/v1', methods = ['GET'])
def dm_messages():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    return dumps(dm_messages_v1(token, dm_id,start))

# dm leave
@APP.route('/dm/leave/v1', methods = ['POST'])
def dm_leave():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    persist_data()
    return dumps(dm_leave_v1(token, dm_id))

# dm remove
@APP.route('/dm/remove/v1', methods = ['DELETE'])
def dm_remove():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    persist_data()
    return dumps(dm_remove_v1(token, dm_id))

# message sendlater
@APP.route('/message/sendlater/v1', methods = ['POST'])
def message_sendlater():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    time_sent = data['time_sent']
    persist_data()
    return dumps(message_sendlater_v1(token, channel_id, message, time_sent))

# message sendlaterdm
@APP.route('/message/sendlaterdm/v1', methods = ['POST'])
def message_sendlaterdm():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    message = data['message']
    time_sent = data['time_sent']
    persist_data()
    return dumps(message_sendlaterdm_v1(token, dm_id, message, time_sent))

# message react
@APP.route('/message/react/v1', methods = ['POST'])
def message_react():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']
    persist_data()
    return dumps(message_react_v1(token, message_id, react_id))

# message unreact
@APP.route('/message/unreact/v1', methods = ['POST'])
def message_unreact():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']
    persist_data()
    return dumps(message_unreact_v1(token, message_id, react_id))


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port 

