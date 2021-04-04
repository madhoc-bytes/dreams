"""HTTP message file"""

# Imports
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_share_v1
from src.data import messages
from src.error import InputError
from flask import Flask, request
from json import dumps

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
