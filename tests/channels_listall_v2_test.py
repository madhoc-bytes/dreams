# Test file for channels_listall_v1

# Imports
import pytest
from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v2, channels_listall_v2
from src.other import clear_v1
from src.error import InputError, AccessError

# Test for a list with no channels details in it
def test_no_channels_listall():
    clear_v1()
    
    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    user_id = user['auth_user_id']
    
    assert(channels_listall_v2(user_id)) == {'channels': []}

# Test for a list with a unique channel 
def test_unique_channels_listall():
    clear_v1()

    user1_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']

    channel = channels_create_v1(user1_id, "My Unique Channel", True)
    channel_join_v1(user1_id, channel['channel_id'])
    
    assert(channels_listall_v2(user1_id)) == {'channels': [{'name': 'My Unique Channel', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}]}


# Test for a list with exactly two channels in it
def test_double_channels_listall():
    clear_v1()

    user1_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']

    channel1 = channels_create_v1(user1_id, "Channel 1", True)
    channel2 = channels_create_v1(user1_id, "Channel 2", True)

    channel_join_v1(user1_id, channel1['channel_id'])
    channel_join_v1(user1_id, channel2['channel_id'])

    assert(channels_listall_v2(user1_id)) == {'channels': [{'name': 'Channel 1', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}, {'name': 'Channel 2', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}]}
    

# Test where there are 3 channels, in which the user has access to 1
def test_channels_with_user_access():

    clear_v1()

    # Create and register two users
    user1_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    user2_id = auth_register_v1('elonmusk@yahoo.com', 'bitcoin777', 'Elon', 'Musk')['auth_user_id']

    # Channels
    channel1 = channels_create_v1(user1_id, "Jack Channel", True)
    channel2 = channels_create_v1(user2_id, "Elon Channel 1", True)
    channel3 = channels_create_v1(user2_id, "Elon Channel 2", True)

    channel_join_v1(user1_id, channel1['channel_id'])
    channel_join_v1(user2_id, channel2['channel_id'])
    channel_join_v1(user2_id, channel3['channel_id'])
    
    assert channels_listall_v2(user1_id) == {'channels': [{'name': 'Jack Channel', 'all_members': [{'name_first': 'Jack', 'name_last': 'Germani', 'u_id': 0}]}, {'name': 'Elon Channel 1', 'all_members': [{'name_first': 'Elon', 'name_last': 'Musk', 'u_id': 1}]}, {'name': 'Elon Channel 2', 'all_members': [{'name_first': 'Elon', 'name_last': 'Musk', 'u_id': 1}]}]}