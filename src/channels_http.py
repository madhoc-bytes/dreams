"""HTTP channels file"""

# Imports
from src import server
from src.channels import channels_list_v2, channels_listall_v2
from src.data import channels, users
from src.error import InputError
from flask import Flask, request
from json import dumps

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



