'''Test file for message_edit_v1.py'''

# Imports
import pytest
from src.message import message_edit_v1, message_send_v2, is_message_edited
from src.data import users, channels
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from src.error import InputError, AccessError


# Message is more than 1000 characters
def test_message_too_long():

    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])
    message = 'Valid message!'
    new_long_message = 'a' * 1001

    message_one_id = message_send_v2(token, channel, message) 

    # Assertions: InputError
    with pytest.raises(InputError):
        message_edit_v1(token, message_one_id, new_long_message)
    


# Test normal message with authorised user in channel
def test_valid_message_edit():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])
    message = 'Valid message!'
    new_message = 'This message was edited'

    message_one_id = message_send_v2(token, channel, message) 
    message_edit_v1(token, message_one_id, new_message)

    message_test = is_message_edited(message_one_id, new_message)

    assert message_test == True 


def test_message_edit_two_messages():
    # Reset
    clear_v2()

    token_1 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel_1 = channels_create_v2(token_1, 'Channel 1', True)
    channel_join_v2(token_1, channel_1['channel_id'])

    
    message_2 = 'Another valid message'
    new_message = 'This message was edited'


    message_two_id = message_send_v2(token_1, channel_1, message_2)

    message_edit_v1(token_1, message_two_id, new_message)

    message_test = is_message_edited(message_two_id, new_message)

    assert message_test == True 


def test_message_edit_two_channels():
    # Reset
    clear_v2()

    token_1 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('test@yahoo.com', 'jack123', 'Test', 'Germani')['token']

    channel_1 = channels_create_v2(token_1, 'Channel 1', True)
    channel_2 = channels_create_v2(token_2, 'Channel 2', True)

    channel_join_v2(token_1, channel_1['channel_id'])
    channel_join_v2(token_2, channel_2['channel_id'])


    message_2 = 'Another valid message'
    new_message = 'This message was edited'

    
    message_two_id = message_send_v2(token_2, channel_2, message_2)

    message_edit_v1(token_2, message_two_id, new_message)

    message_test = is_message_edited(message_two_id, new_message)

    assert message_test == True


def test_message_edit_not_sent_by_user():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('test@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])
    channel_join_v2(token_2, channel['channel_id'])

    message = 'Valid message!'
    new_message = 'This message was edited'

    message_one_id = message_send_v2(token, channel, message) 


    with pytest.raises(AccessError):
        message_edit_v1(token_2, message_one_id, new_message)





