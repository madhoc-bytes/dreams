'''Test file for message_send_v1.py'''

# Imports
import pytest
from message import message_send_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from error import InputError, AccessError


# Message is more than 1000 characters
def test_message_too_long():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])
    message = 'a' * 1001

    # Assertions: InputError
    assert message_send_v1(user_id, channel, message) == 'Message is more than 1000 characters'
    

# Authorised user did not join channel 
def test_not_authorised_user():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    message = 'Valid Message!'

    # Assertions: InputError
    assert message_send_v1(user_id, channel, message) == 'User is not authorised to this channel'

# Test normal message with authorised user in channel
def test_one_message():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])
    message = 'Valid message!'

    # Assertions: InputError
    assert message_send_v1(user_id, channel, message) == {1}


# Test normal message with authorised user in channel
def test_two_messages():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])
    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'

    # Send first message
    message_send_v1(user_id, channel, message_one)

    # Assertion
    assert message_send_v1(user_id, channel, message_two) == {2}


