import pytest

from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_details_v2
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.dm import dm_create_v1
from src.search import search_v2
from src.message_senddm_v2 import message_senddm_v2
from src.error import InputError, AccessError
from src.other import clear_v2

def test_system():
    clear_v2()

    # register 1 user
    user = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_user',
        'test_lname_user'
    )

    assert search_v2(user['token'], 'test') == {'messages': []}  

    # create a test channel
    test_channel_id = channels_create_v2(user['token'], 'test_channel_1', True)['channel_id']

    # add auth to the test channel
    channel_join_v2(user['token'], test_channel_id)

    # send a message
    message_send_v2(user['token'], test_channel_id, "test_msg1")
    message_send_v2(user['token'], test_channel_id, "test_msg2")
    message_send_v2(user['token'], test_channel_id, "random_msg1")

    assert search_v2(user['token'], 'test') == {
        'messages': [
            "test_msg1",
            "test_msg2"
        ]
    }

    #create dm
    dm_data = dm_create_v1(user['token'], [])

    message_senddm_v2(user['token'], dm_data['dm_id'], "test_msg3")
    message_senddm_v2(user['token'], dm_data['dm_id'], "test_msg4")

    assert search_v2(user['token'], 'test') == {
        'messages': [
            "test_msg1",
            "test_msg2",
            "test_msg3",
            "test_msg4"
        ]
    }

def test_long_querystr():
    clear_v2()

    # register 1 user
    user = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_user',
        'test_lname_user'
    )
    long_str = 'a' * 1001

    with pytest.raises(InputError):
        search_v2(user['token'], long_str) 


    
    