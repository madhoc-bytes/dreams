'''Test file for message_remove_v1.py'''

# Imports
import pytest
from src.message import message_edit_v1, message_send_v1, message_remove_v1, is_message_deleted
from src.data import users, channels
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError, AccessError


def test_remove_one_message():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])

    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'

    # Send two message
    message_one_id = message_send_v1(user_id, channel, message_one)
    message_two_id = message_send_v1(user_id, channel, message_two)

    # Delete message 1
    message_remove_v1(user_id, message_one_id)
    result = is_message_deleted(message_one_id) 

    # Assertion
    assert result == True


def test_remove_two_messages():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])

    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'
    message_three = 'I will not be deleted!'

    # Send two message
    message_one_id = message_send_v1(user_id, channel, message_one)
    message_two_id = message_send_v1(user_id, channel, message_two)
    message_three_id = message_send_v1(user_id, channel, message_three)

    # Delete message 1 and 2
    message_remove_v1(user_id, message_one_id)
    message_remove_v1(user_id, message_two_id)

    result_one = is_message_deleted(message_one_id) 
    result_two = is_message_deleted(message_two_id)

    # Assertion
    assert result_one == True and result_two == True
    

def test_remove_two_messages_two_channels():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    user_id_2 = auth_register_v1('test@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_2 = channels_create_v1(user_id_2, 'My Channel 2', True)
    channel_join_v1(user_id, channel['channel_id'])
    channel_join_v1(user_id_2, channel_2['channel_id'])

    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'
    message_three = 'I will not be deleted!'

    # Send two message
    message_one_id = message_send_v1(user_id, channel, message_one)
    message_two_id = message_send_v1(user_id_2, channel_2, message_two)
    message_three_id = message_send_v1(user_id, channel, message_three)

    # Delete message 1 and 2
    message_remove_v1(user_id, message_one_id)
    message_remove_v1(user_id_2, message_two_id)

    result_one = is_message_deleted(message_one_id) 
    result_two = is_message_deleted(message_two_id)

    # Assertion
    assert result_one == True and result_two == True


def test_remove_deleted_message():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])

    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'

    # Send two message
    message_one_id = message_send_v1(user_id, channel, message_one)
    message_two_id = message_send_v1(user_id, channel, message_two)

    # Delete message 1
    message_remove_v1(user_id, message_one_id)

    # Assertion
    with pytest.raises(InputError):
        message_remove_v1(user_id, message_one_id)


def test_remove_message_not_sent_by_same_user():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    user_id_2 = auth_register_v1('test@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])
    channel_join_v1(user_id_2, channel['channel_id'])

    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'

    # Send two message
    message_one_id = message_send_v1(user_id, channel, message_one)
    message_two_id = message_send_v1(user_id_2, channel, message_two)


    # Assertion
    with pytest.raises(AccessError):
        message_remove_v1(user_id, message_two_id)