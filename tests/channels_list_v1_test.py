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
    channel = channels_create_v1(user_id, 'My Unique Channel', True)
    channel_join_v1(user_id, channel['channel_id'])

    assert(channels_list_v1(user_id) == [{'name': 'My Unique Channel',
                                        'all_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ]
                                        
                                        }])



# Test for a list with exactly two channels in it
def test_two_channels_in_list():
    clear_v1()
    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']

    channel1 = channels_create_v1(user_id, 'Channel 1', True)
    channel2 = channels_create_v1(user_id, 'Channel 2', True)
    channel_join_v1(user_id, channel1['channel_id'])
    channel_join_v1(user_id, channel2['channel_id'])


    assert(channels_list_v1(user_id) == [{'name': 'Channel 1',
                                        'all_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ]
                                        
                                        }, {
                                           'name': 'Channel 2',
                                        
                                        'all_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ] 
                                        }])


# Test where user is authorized to access 1 channel, when there are 2 channels in total
def test_two_users_channels_list():
    clear_v1()

    # Create and register two different users
    user1_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    user2_id = auth_register_v1('elonmusk@yahoo.com', 'bitcoin777', 'Elon', 'Musk')['auth_user_id']

    # Create two channels: one ofr user 1 and one for user 2
    channel1 = channels_create_v1(user1_id, "Jack Channel", True)
    channel2 = channels_create_v1(user2_id, "Elon Channel", True)

    channel_join_v1(user1_id, channel1['channel_id'])
    channel_join_v1(user2_id, channel2['channel_id'])

    assert(channels_list_v1(user1_id) == [{'name': 'Jack Channel',
                                        'all_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ]
                                        
                                        }])


# Test where user is part of no channels, and there are 2 different channels available
def test_two_users_not_in_channels():
    clear_v1()

    # registers two seperate users
    user1_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    user2_id = auth_register_v1('elonmusk@yahoo.com', 'bitcoin777', 'Elon', 'Musk')['auth_user_id']


    # Create two channels: one ofr user 1 and one for user 2
    channel1 = channels_create_v1(user2_id, "Elon Channel 1", True)
    channel2 = channels_create_v1(user2_id, "Elon Channel 2", True)

    channel_join_v1(user2_id, channel1['channel_id'])
    channel_join_v1(user2_id, channel2['channel_id'])

    channel_list = channels_list_v1(user1_id)
    length = len(channel_list)

    assert length == 0 