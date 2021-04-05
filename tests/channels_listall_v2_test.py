# Test file for channels_listall_v2

# Imports
import pytest
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.other import clear_v2
from src.error import InputError, AccessError

# Test for a list with no channels details in it
def test_no_channels_listall():
    clear_v2()
    
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    assert(channels_listall_v2(token)) == {'channels': []}

# Test for a list with a unique channel 
def test_unique_channels_listall():
    clear_v2()

    token_1 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    channel = channels_create_v2(token_1, "My Unique Channel", True)
    channel_join_v2(token_1, channel['channel_id'])
    
    assert(channels_listall_v2(token_1)) == {'channels': [{'name': 'My Unique Channel', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}]}


# Test for a list with exactly two channels in it
def test_double_channels_listall():
    clear_v2()

    token_1 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    channel1 = channels_create_v2(token_1, "Channel 1", True)
    channel2 = channels_create_v2(token_1, "Channel 2", True)

    channel_join_v2(token_1, channel1['channel_id'])
    channel_join_v2(token_1, channel2['channel_id'])

    assert(channels_listall_v2(token_1)) == {'channels': [{'name': 'Channel 1', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}, {'name': 'Channel 2', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}]}
    

# Test where there are 3 channels, in which the user has access to 1
def test_channels_with_user_access():

    clear_v2()

    # Create and register two users
    token_1 = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('elonmusk@yahoo.com', 'bitcoin777', 'Elon', 'Musk')['token']

    # Channels
    channel1 = channels_create_v2(token_1, "Jack Channel", True)
    channel2 = channels_create_v2(token_2, "Elon Channel 1", True)
    channel3 = channels_create_v2(token_2, "Elon Channel 2", True)

    channel_join_v2(token_1, channel1['channel_id'])
    channel_join_v2(token_2, channel2['channel_id'])
    channel_join_v2(token_2, channel3['channel_id'])
    
    assert channels_listall_v2(token_1) == {'channels': [{'name': 'Jack Channel', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}, {'name': 'Elon Channel 1', 'all_members': [{'name_first': 'Elon', 'name_last': 'Musk', 'u_id': 1}]}, {'name': 'Elon Channel 2', 'all_members': [{'name_first': 'Elon', 'name_last': 'Musk', 'u_id': 1}]}]}