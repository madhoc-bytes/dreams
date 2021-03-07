# Test file for channels_listall_v1

# Imports
import pytest
from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.other import clear_v1
from src.error import InputError, AccessError

# Test for a list with no channels details in it
def test_no_channels_listall():
    clear_v1()
    
    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    id = user['auth_user_id']
    
    channel_list = channels_listall_v1(id)
    assert bool(channel_list) == False

# Test for a list with a unique channel 
def test_unique_channels_listall():
    clear_v1()

    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    id = user['auth_user_id']

    channels_create_v1(id, "My Unique Channel", True)
    
    assert(channels_listall_v1(id) == [{'name': 'My Unique Channel', 'owner_members': [], 'all_members': [0]}])


# Test for a list with exactly two channels in it
def test_double_channels_listall():
    clear_v1()

    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    id = user['auth_user_id']

    channels_create_v1(id, "Channel 1", True)
    channels_create_v1(id, "Channel 2", True)

    assert(channels_listall_v1(id) == [{'name': 'Channel 1', 'owner_members': [], 'all_members': [0]}, {'name': 'Channel 2', 'owner_members': [], 'all_members': [0]}])


