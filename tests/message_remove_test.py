'''Test file for message_remove_v1.py'''

# Imports
import pytest
from src.message import message_edit_v1, message_send_v1, message_remove_v1, is_message_deleted
from src.data import users, channels, dms
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from src.error import InputError, AccessError
from src.dm import dm_create_v1
from src.message_senddm_v2 import message_senddm_v2


def test_remove_one_message_from_channel():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])

    message_one = 'I am message #1'


    # Send two message
    message_one_id = message_send_v1(token, channel, message_one)


    # Delete message 1
    message_remove_v1(token, message_one_id)
    result = is_message_deleted(message_one_id) 

    # Assertion
    assert result == True

def test_remove_two_messages_from_channel():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])

    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'


    # Send two message
    message_one_id = message_send_v1(token, channel, message_one)
    message_two_id = message_send_v1(token, channel, message_two)

    # Delete message 1 and 2
    message_remove_v1(token, message_one_id)
    message_remove_v1(token, message_two_id)

    result_one = is_message_deleted(message_one_id) 
    result_two = is_message_deleted(message_two_id)

    # Assertion
    assert result_one == True and result_two == True

def test_remove_two_messages_two_channels():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('test@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_2 = channels_create_v2(token_2, 'My Channel 2', True)
    channel_join_v2(token, channel['channel_id'])
    channel_join_v2(token_2, channel_2['channel_id'])

    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'
    

    # Send two message
    message_one_id = message_send_v1(token, channel, message_one)
    message_two_id = message_send_v1(token_2, channel_2, message_two)


    # Delete message 1 and 2
    message_remove_v1(token, message_one_id)
    message_remove_v1(token_2, message_two_id)

    result_one = is_message_deleted(message_one_id) 
    result_two = is_message_deleted(message_two_id)

    # Assertion
    assert result_one == True and result_two == True

def test_remove_deleted_message_channel():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])

    message_one = 'I am message #1'


    # Send two message
    message_one_id = message_send_v1(token, channel, message_one)
    

    # Delete message 1
    message_remove_v1(token, message_one_id)

    # Assertion
    with pytest.raises(InputError):
        message_remove_v1(token, message_one_id)

def test_remove_message_not_sent_by_same_user():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('test@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])
    channel_join_v2(token_2, channel['channel_id'])

    message_two = 'Hello!'

    # Send two message
    message_two_id = message_send_v1(token_2, channel, message_two)


    # Assertion
    with pytest.raises(AccessError):
        message_remove_v1(token, message_two_id)

def test_remove_message_from_dm():
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
    message_remove_v1(token, message_one_id)
    result = is_message_deleted(message_one_id) 

    # Assertion
    assert result == True