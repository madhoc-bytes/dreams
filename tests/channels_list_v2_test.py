# Test file for channels_list_v2

# Imports
import pytest
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.other import clear_v2
from src.error import InputError, AccessError


# Test for a list without any channel details in it

def test_no_channels_in_list():
    clear_v2()
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    assert(channels_list_v2(token)) == {'channels': []}



# Test for a list with only one channel details in it
def test_one_channel_in_list():
    clear_v2()
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    channel = channels_create_v2(token, 'My Unique Channel', True)
    channel_join_v2(token, channel['channel_id'])

    assert(channels_list_v2(token)) == {'channels': [{'name': 'My Unique Channel', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}]}
    


# Test for a list with exactly two channels in it
def test_two_channels_in_list():
    clear_v2()
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    channel1 = channels_create_v2(token, 'Channel 1', True)
    channel2 = channels_create_v2(token, 'Channel 2', True)
    channel_join_v2(token, channel1['channel_id'])
    channel_join_v2(token, channel2['channel_id'])

    assert(channels_list_v2(token)) == {'channels': [{'name': 'Channel 1', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}, {'name': 'Channel 2', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}]}
    


# Test where user is authorized to access 1 channel, when there are 2 channels in total
def test_two_users_channels_list():
    clear_v2()

    # Create and register two different users
    token_1 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('elonmusk@yahoo.com', 'bitcoin777', 'Elon', 'Musk')['token']

    # Create two channels: one ofr user 1 and one for user 2
    channel1 = channels_create_v2(token_1, "Jack Channel", True)
    channel2 = channels_create_v2(token_2, "Elon Channel", True)

    channel_join_v2(token_1, channel1['channel_id'])
    channel_join_v2(token_2, channel2['channel_id'])

    assert(channels_list_v2(token_1) == {'channels': [{'name': 'Jack Channel', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}]})


# Test where user is part of no channels, and there are 2 different channels available
def test_two_users_not_in_channels():
    clear_v2()

    # registers two seperate users
    token_1 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('elonmusk@yahoo.com', 'bitcoin777', 'Elon', 'Musk')['token']

    # Create two channels: one ofr user 1 and one for user 2
    channel1 = channels_create_v2(token_2, "Elon Channel 1", True)
    channel2 = channels_create_v2(token_2, "Elon Channel 2", True)

    channel_join_v2(token_2, channel1['channel_id'])
    channel_join_v2(token_2, channel2['channel_id'])

    assert(channels_list_v2(token_1)) == {'channels': []}