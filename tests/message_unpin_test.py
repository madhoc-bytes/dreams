'''Test file for message_unpin_v1.py'''

# Imports
import pytest
from src.message import message_send_v2, is_message_deleted, message_unpin_v1, message_pin_v1, message_is_unpinned
from src.data import users, channels, dms
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from src.error import InputError, AccessError
from src.dm import dm_create_v1
from src.message_senddm_v2 import message_senddm_v2


def test_unpin_one_message_from_channel():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])

    message_one = 'I am message #1'

    # Send two message
    message_one_id = message_send_v2(token, channel, message_one)

    # Delete message 1
    message_pin_v1(token, message_one_id)
    message_unpin_v1(token, message_one_id)
    result = message_is_unpinned(message_one_id) 

    # Assertion
    assert result == True

def test_unpin_one_message_from_dm():
    # Reset
    clear_v2()

    user = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    token = user['token']
    auth_user_id = user['auth_user_id']
    u_ids = [auth_user_id]
    dm_id_1 = dm_create_v1(token, u_ids)['dm_id']

    message_one = 'I am message #1'
    

    # Send two message
    message_one_id = message_senddm_v2(token, dm_id_1, message_one)

    # Delete message 1
    message_pin_v1(token, message_one_id)
    message_unpin_v1(token, message_one_id)
    result = message_is_unpinned(message_one_id) 

    # Assertion
    assert result == True

def test_unpin_not_existant_message():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])


    # Assertion
    with pytest.raises(InputError):
        message_unpin_v1(token, 42)

def test_unpin_user_not_in_channel():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token2 = auth_register_v2('test234@yahoo.com', 'test1234', 'Jack', 'Germani')['token']

    channel = channels_create_v2(token, 'My Channel', True)
    channel2 = channels_create_v2(token2, 'Channel 2', True)

    channel_join_v2(token, channel['channel_id'])
    channel_join_v2(token2, channel2['channel_id'])

    message_one = 'I am message #1'
    message_two = 'Message 2'

    # Send two message
    message_one_id = message_send_v2(token, channel, message_one)
    message_two_id = message_send_v2(token2, channel2, message_two)

    message_pin_v1(token, message_one_id)

    with pytest.raises(AccessError):
        message_unpin_v1(token2, message_one_id)

def test_pin_user_not_in_dm():
    clear_v2()

    user = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    token = user['token']

    user2 = auth_register_v2('test@yahoo.com', 'jack123', 'Jack', 'Germani')
    token2 = user2['token']

    auth_user_id_1 = user['auth_user_id']
    auth_user_id_2 = user2['auth_user_id']
    u_ids = [auth_user_id_1]
    dm_id_1 = dm_create_v1(token, u_ids)['dm_id']

    message_one = 'I am message #1'
    

    # Send two messages
    message_one_id = message_senddm_v2(token, dm_id_1, message_one)
    message_pin_v1(token, message_one_id)

    with pytest.raises(AccessError):
        message_unpin_v1(token2, message_one_id)
