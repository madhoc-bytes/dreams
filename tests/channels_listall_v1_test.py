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

    user1_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')

    channel = channels_create_v1(user1_id, "My Unique Channel", True)
    channel_join_v1(user1_id, {'id': channel['id']})
    
    assert(channels_listall_v1(user1_id) == [{'name': 'My Unique Channel',
                                        'owner_members': [
                                            {}
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ]
                                        
                                        }])


# Test for a list with exactly two channels in it
def test_double_channels_listall():
    clear_v1()

    user1_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')

    channel1 = channels_create_v1(user1_id, "Channel 1", True)
    channel2 = channels_create_v1(user1_id, "Channel 2", True)

    channel_join_v1(user1_id, {'id': channel1['id']})
    channel_join_v1(user1_id, {'id': channel2['id']})

    assert(channels_listall_v1(user1_id) == [{'name': 'Channel 1',
                                        'owner_members': [
                                            {}
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ]
                                        
                                        }, {
                                           'name': 'Channel 2',
                                        'owner_members': [
                                            {}
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ] 
                                        }])


# Test where there are 3 channels, in which the user has access to 1
def test_channels_with_user_access():

    clear_v1()

    # Create and register two users
    user1_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')
    user2_id = auth_register_v1('elonmusk@yahoo.com', 'bitcoin777', 'Elon', 'Musk')

    # Channels
    channel1 = channels_create_v1(user1_id, "Jack Channel", True)
    channel2 = channels_create_v1(user2_id, "Elon Channel 1", True)
    channel3 = channels_create_v1(user2_id, "Elon Channel 2", True)

    channel_join_v1(user1_id, {'id': channel1['id']})
    channel_join_v1(user2_id, {'id': channel2['id']})
    channel_join_v1(user2_id, {'id': channel3['id']})
    
    assert(channels_listall_v1(user1_id) == [{'name': 'Jack Channel',
                                        'owner_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': 0,
                                                'name_first': 'Jack',
                                                'name_last': 'Germani',
                                            }
                                        ]
                                        
                                        }, {
                                           'name': 'Elon Channel 1',
                                        'owner_members': [
                                            {
                                                'u_id': 1,
                                                'name_first': 'Elon',
                                                'name_last': 'Musk',
                                            }
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': 1,
                                                'name_first': 'Elon',
                                                'name_last': 'Musk',
                                            }
                                        ] 
                                        }, {
                                            'name': 'Elon Channel 2',
                                        'owner_members': [
                                            {
                                                'u_id': 1,
                                                'name_first': 'Elon',
                                                'name_last': 'Musk',
                                            }
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': 1,
                                                'name_first': 'Elon',
                                                'name_last': 'Musk',
                                            }
                                        ]
                                        }])