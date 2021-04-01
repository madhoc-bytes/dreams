"""HTTP message file"""

# Imports
from src.message import message_send_v1, message_edit_v1, message_remove_v1
from src.channel import test_if_user_in_ch
from src.data import channels
from src.error import InputError
from flask import Flask, request
from json import dumps

# message/send/v1
@APP.route('/message/send/v1', methods=['POST'])
def channels_list_v1():

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    return_value = message_send_v1(token, channel_id, message)
    return dumps(return_value)

# message/edit/v1
@APP.route('/message/edit/v1', methods=['PUT'])
def channels_list_v1():

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    return_value = message_edit_v1(token, channel_id, message)
    return dumps(return_value)

# message/remove/v1
@APP.route('/message/remove/v1', methods=['DELETE'])
def channels_list_v1():

    token = request.form.get('token')
    message_id = request.form.get('message_id')

    return_value = message_remove_v1(token, message_id)
    return dumps(return_value)