"""HTTP channels file"""

# Imports
from src.channel import test_if_user_in_ch
from src.data import channels
from src.error import InputError
from flask import Flask, request
from json import dumps

# channels/list/v2
@APP.route('/channels/list/v2', methods=['GET'])
def channels_list_v1():
    """Function that lists all channels for which a certain user has access"""

    token = request.form.get('token')
    return_value = channels_list_v2(token)
    return dumps(return_value)


# channels/listall/v2
@APP.route('/channels/listall/v2', methods=['GET'])
def channels_listall_v1():
    """Function that lists all channels"""

    token = request.form.get('token')
    return_value = channels_listall_v1(token)
    return dumps(return_value)



