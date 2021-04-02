'''Test file for message_send_v1.py'''

# Imports
import pytest
from message import message_edit_v1, message_send_v1, is_message_edited
from src.data import users, channels
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from error import InputError, AccessError


# Message is more than 1000 characters
def test_message_too_long():

    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])
    message = 'Valid message!'
    new_long_message = 'a' * 1001

    message_one_id = message_send_v1(user_id, channel, message) 

    assert message_edit_v1(user_id, message_one_id, new_long_message) == 'Message is more than 1000 characters' 
    


# Test normal message with authorised user in channel
def test_valid_message_edit():
    # Reset
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    channel = channels_create_v1(user_id, 'My Channel', True)
    channel_join_v1(user_id, channel['channel_id'])
    message = 'Valid message!'
    new_message = 'This message was edited'

    message_one_id = message_send_v1(user_id, channel, message) 
    message_edit_v1(user_id, message_one_id, new_message)

    message_test = is_message_edited(message_one_id, new_message)

    assert message_test == True 





