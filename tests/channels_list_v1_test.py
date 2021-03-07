# Test file for channels_list_v1

# Imports
import pytest
from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.other import clear_v1
from src.error import InputError, AccessError


# Test for a list without any channel details in it
def test_no_channels_in_list():
    clear_v1()
    user = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    id = user['auth_user_id']
    
    channel_list = channels_list_v1(id)
    assert bool(channel_list) == False


# Test for a list with only one channel details in it
def test_one_channel_in_list():
    clear_v1()
    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']

    channels_create_v1(user_id, 'My Unique Channel', True)

    assert(channels_list_v1(user_id) == {'name': 'My Unique Channel',
                                        'owner_members': [
                                            {
                                                'u_id': user_id,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': user_id,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ]
                                        
                                        })



# Test for a list with exactly two channels in it
def test_two_channels_in_list():
    clear_v1()
    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']

    channel_list = []

    channels_create_v1(user_id, 'Channel 1', True)
    channels_create_v1(user_id, 'Channel 2', True)

    assert(channels_list_v1(user_id) == [{'name': 'Channel 1',
                                        'owner_members': [
                                            {
                                                'u_id': user_id,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': user_id,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ]
                                        
                                        }])

