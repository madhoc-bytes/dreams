import pytest
from src.data import channels, users, dms
from src.message import message_send_v1, message_react_v1
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v2, channel_messages_v2
from src.other import clear_v2
from src.error import AccessError, InputError

def test_react_basic():
    clear_v2()
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    test_channel = channels_create_v2(auth_token, "test channel", True)['channel_id']
    channel_join_v2(auth_token, test_channel)

    message_send_v1(auth_token, test_channel, 'message')

    message_react_v1(auth_token, 0, 1)

    test_message = channel_messages_v2(auth_token, test_channel , 0)['messages']
    reacts = test_message[0]['reacts']
    assert reacts == [{
        'react_id': 1,
        'u_ids': [0],
        'is_this_user_reacted': True
    }]

def test_react_invalidmid():
    clear_v2()

    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    
    with pytest.raises(InputError):
        message_react_v1(auth_token, 1, 1)

def test_react_invalidreactid():
    clear_v2()

    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    test_channel = channels_create_v2(auth_token, "test channel", True)['channel_id']
    channel_join_v2(auth_token, test_channel)

    message_send_v1(auth_token, test_channel, 'message')

    with pytest.raises(InputError):
        message_react_v1(auth_token, 0, 2)

def test_already_reacted():
    clear_v2()
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    test_channel = channels_create_v2(auth_token, "test channel", True)['channel_id']
    channel_join_v2(auth_token, test_channel)

    message_send_v1(auth_token, test_channel, 'message')

    message_react_v1(auth_token, 0, 1)   

    with pytest.raises(InputError):
        message_react_v1(auth_token, 0, 1)