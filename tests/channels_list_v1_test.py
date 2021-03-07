# Test file for channels_list_v1

import pytest
from src.error import InputError
from src import channels
from src import auth
from src import channel
from src import other


def test_valid_channel_details():
    clear_v1()
    valid_email, valid_password, valid_name_first, valid_name_last = 'abc@def.com', 'passWord1', 'jack', 'germani'
    valid_user_id = auth.auth_resgister_v1(valid_email, valid_password, valid_name_first, valid_name_last)


    valid_channel_name = 'jack_channel'
    is_public = True
    valid_channel_id = channels_create_v1(valid_user_id, valid_channel_name, is_public)

    check_valid_channel_details = channels_details_v1(valid_user_id, valid_channel_id)

    assert check_valid_channel_details == ('jack_channel', 'jackgermani', 'jackgermani')

def test_no_channels_list():
    clear_v1()
    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    id = user['auth_user_id']
    
    user_list = channels_list_v1(id)
    assert bool(user_list['channels']) == False


def test_unique_channels_list():
    clear_v1()
    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    id = user['auth_user_id']

    channels_create_v1(id, 'Jacks Channel', True)

    user_list = channels_list_v1(id)
    length = len(user_list['channels'])
    assert (length == 1)
