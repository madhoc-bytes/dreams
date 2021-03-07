# Test file for channels_listall_v1

import pytest
from src.error import InputError
from src import channels
from src import auth
from src import channel
from src import other

def test_no_channels_listall():
    clear_v1()
    
    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    id = user['auth_user_id']
    
    user_list = channels_listall_v1(id)
    assert (bool(user_list['channels']) == False)


def test_unique_channels_listall():
    clear_v1()

    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    id = user['auth_user_id']

    channels_create_v1(id, "Single Channel", True)
    user_list = channels_listall(id)
    length = len(user_list['channels'])
    assert (length == 1)