"""HTTP message file"""

# Imports
from src.message import message_send_v1, message_edit_v1, message_remove_v1
from src.data import messages
from src.error import InputError
from flask import Flask, request
from json import dumps

# message/send/v1
@APP.route('/message/send/v1', methods=['POST'])
def send_message():

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    return_value = message_send_v1(token, channel_id, message)
    return dumps(return_value)

# message/edit/v1
@APP.route('/message/edit/v1', methods=['PUT'])
def edit_message():

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    return_value = message_edit_v1(token, channel_id, message)
    return dumps(return_value)

# message/remove/v1
@APP.route('/message/remove/v1', methods=['DELETE'])
def remove_message():

    token = request.form.get('token')
    message_id = request.form.get('message_id')

    return_value = message_remove_v1(token, message_id)
    return dumps(return_value)