'''Test file for message_send_v1.py'''

# Imports
import pytest
from src.data import channels, users, dms
from src.message import message_send_v1, is_message_shared
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from src.error import InputError, AccessError


# Message is more than 1000 characters
def test_message_too_long():
    # Reset
    clear_v2()
    
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])
    message = 'a' * 1001

    # Assertions: InputError
    with pytest.raises(InputError):
        message_send_v1(token, channel, message)
        
    

# Authorised user did not join channel 
def test_not_authorised_user():
    # Reset
    clear_v2()

    token_1 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('test@yahoo.com', 'test123', 'Travis', 'Germani')['token']
    token_3 = auth_register_v2('test2@yahoo.com', 'test123', 'Travis', 'Germani')['token']

    channel1 = channels_create_v2(token_1, 'Channel 1', True)
    channel2 = channels_create_v2(token_2, 'Channel 2', True)
    channel3 = channels_create_v2(token_3, 'Channel 3', True)

    channel_join_v2(token_1, channel1['channel_id'])
    channel_join_v2(token_2, channel2['channel_id'])
    channel_join_v2(token_3, channel3['channel_id'])

    message = 'Valid Message!'

    # Assertions: AccessError
    with pytest.raises(AccessError):
        message_send_v1(token_1, channel2, message)


# Test normal message with authorised user in channel
def test_one_message():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])
    message = 'Valid message!'

    # Assertions: InputError
    message_id = message_send_v1(token, channel, message)
    exists = is_message_shared(message_id, channel)
    assert exists == True and message_id == {'message_id': 0}


def test_two_messages():
    # Reset
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Channel', True)
    channel_join_v2(token, channel['channel_id'])
    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'

    # Send first message
    message_id_1 = message_send_v1(token, channel, message_one)
    message_id_2 = message_send_v1(token, channel, message_two)
    
    exists1 = is_message_shared(message_id_1, channel)
    exists2 = is_message_shared(message_id_2, channel) 

    # Assertion
    assert exists1 == True and exists2 == True and message_id_2 == {'message_id': 1}


def test_two_messages_channels():
    # Reset
    clear_v2()

    token_1 = auth_register_v2('test@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    channel_1 = channels_create_v2(token_1, 'My Channel 1', True)
    channel_2 = channels_create_v2(token_2, 'My Channel 2', True)

    channel_join_v2(token_1, channel_1['channel_id'])
    channel_join_v2(token_2, channel_1['channel_id'])
    channel_join_v2(token_2, channel_2['channel_id'])

    message_one = 'I am message #1'
    message_two = 'My ID should be 2!'

    # Send first message
    message_id_1 = message_send_v1(token_1, channel_1, message_one)
    message_id_2 = message_send_v1(token_2, channel_1, message_two)
    
    exists1 = is_message_shared(message_id_1, channel_1)
    exists2 = is_message_shared(message_id_2, channel_1) 
    exists3 = is_message_shared(message_id_2, channel_2)

    # Assertion
    assert exists1 == True and exists2 == True and exists3 == False



